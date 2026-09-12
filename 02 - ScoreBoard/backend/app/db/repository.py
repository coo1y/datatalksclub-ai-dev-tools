"""Query layer: reads `app/db/tables.py` rows and reassembles the camelCase Pydantic
shapes in `app.models` that the routers return. Routers should never import `tables`
or touch a `Session` directly outside of this module.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models import (
    League,
    LeagueSummary,
    Match,
    MatchEvent,
    MatchEventCreate,
    MatchLineups,
    MatchResultLetter,
    MatchScore,
    MatchStatistics,
    MatchUpdate,
    Player,
    Standing,
    Team,
    TeamCompetitionLink,
    TeamLineup,
    TeamMatchStatistics,
    TeamSummary,
)

from .tables import (
    LeagueRow,
    LineupEntryRow,
    MatchEventRow,
    MatchLineupRow,
    MatchRow,
    MatchStatisticsRow,
    PlayerRow,
    TeamCompetitionRow,
    TeamRow,
)

# --- leagues -----------------------------------------------------------------


def _to_league(row: LeagueRow) -> League:
    return League(
        id=row.id,
        name=row.name,
        short_name=row.short_name,
        country=row.country,
        logo_url=row.logo_url,
        scope=row.scope,
        is_supported=row.is_supported,
        season=row.season,
    )


def list_leagues(session: Session) -> List[League]:
    rows = session.exec(select(LeagueRow)).all()
    return [_to_league(row) for row in rows]


def get_league(session: Session, league_id: str) -> Optional[League]:
    row = session.get(LeagueRow, league_id)
    return _to_league(row) if row else None


# --- teams ---------------------------------------------------------------------


def _competitions_by_team(session: Session, team_ids: Sequence[str]) -> Dict[str, List[TeamCompetitionLink]]:
    if not team_ids:
        return {}
    rows = session.exec(select(TeamCompetitionRow).where(TeamCompetitionRow.team_id.in_(team_ids))).all()
    grouped: Dict[str, List[TeamCompetitionLink]] = defaultdict(list)
    for row in rows:
        grouped[row.team_id].append(TeamCompetitionLink(league_id=row.league_id, scope=row.scope))
    return grouped


def _to_team(row: TeamRow, competitions: List[TeamCompetitionLink]) -> Team:
    return Team(
        id=row.id,
        name=row.name,
        short_name=row.short_name,
        crest_url=row.crest_url,
        country=row.country,
        competitions=competitions,
        is_popular=row.is_popular or None,
    )


def list_teams(session: Session, league_id: Optional[str] = None, query: Optional[str] = None) -> List[Team]:
    team_rows = session.exec(select(TeamRow)).all()

    if league_id:
        matching_team_ids = {
            row.team_id
            for row in session.exec(select(TeamCompetitionRow).where(TeamCompetitionRow.league_id == league_id)).all()
        }
        team_rows = [row for row in team_rows if row.id in matching_team_ids]

    if query:
        needle = query.strip().lower()
        team_rows = [row for row in team_rows if needle in row.name.lower() or needle in row.short_name.lower()]

    competitions = _competitions_by_team(session, [row.id for row in team_rows])
    return [_to_team(row, competitions.get(row.id, [])) for row in team_rows]


def get_team(session: Session, team_id: str) -> Optional[Team]:
    row = session.get(TeamRow, team_id)
    if row is None:
        return None
    competitions = _competitions_by_team(session, [team_id]).get(team_id, [])
    return _to_team(row, competitions)


# --- matches ---------------------------------------------------------------------


def _team_summaries(session: Session, team_ids: Sequence[str]) -> Dict[str, TeamSummary]:
    if not team_ids:
        return {}
    rows = session.exec(select(TeamRow).where(TeamRow.id.in_(set(team_ids)))).all()
    return {row.id: TeamSummary(id=row.id, name=row.name, short_name=row.short_name, crest_url=row.crest_url) for row in rows}


def _league_summaries(session: Session, league_ids: Sequence[str]) -> Dict[str, LeagueSummary]:
    if not league_ids:
        return {}
    rows = session.exec(select(LeagueRow).where(LeagueRow.id.in_(set(league_ids)))).all()
    return {row.id: LeagueSummary(id=row.id, name=row.name, short_name=row.short_name) for row in rows}


def _to_match(row: MatchRow, teams: Dict[str, TeamSummary], leagues: Dict[str, LeagueSummary]) -> Match:
    return Match(
        id=row.id,
        league=leagues[row.league_id],
        season=row.season,
        round=row.round,
        kickoff=row.kickoff,
        status=row.status,
        minute=row.minute,
        stoppage_minute=row.stoppage_minute,
        venue=row.venue,
        home_team=teams[row.home_team_id],
        away_team=teams[row.away_team_id],
        score=MatchScore(home=row.home_score, away=row.away_score),
        last_updated=row.last_updated,
        is_stale=row.is_stale or None,
    )


def list_matches(
    session: Session,
    statuses: Optional[Sequence[str]] = None,
    league_id: Optional[str] = None,
    team_id: Optional[str] = None,
) -> List[Match]:
    """Lightweight match list — events/lineups/statistics are left unset here and only
    populated by `get_match`, since list views never render that level of detail."""
    stmt = select(MatchRow)
    if statuses:
        stmt = stmt.where(MatchRow.status.in_(statuses))
    if league_id:
        stmt = stmt.where(MatchRow.league_id == league_id)
    if team_id:
        stmt = stmt.where((MatchRow.home_team_id == team_id) | (MatchRow.away_team_id == team_id))

    rows = session.exec(stmt).all()
    teams = _team_summaries(session, [t for row in rows for t in (row.home_team_id, row.away_team_id)])
    leagues = _league_summaries(session, [row.league_id for row in rows])
    return [_to_match(row, teams, leagues) for row in rows]


def _to_player(row: PlayerRow) -> Player:
    return Player(
        id=row.id, name=row.name, shirt_number=row.shirt_number, position=row.position, country_code=row.country_code
    )


def _match_events(session: Session, match_id: str) -> Optional[List[MatchEvent]]:
    rows = session.exec(select(MatchEventRow).where(MatchEventRow.match_id == match_id).order_by(MatchEventRow.minute)).all()
    if not rows:
        return None

    player_ids = {pid for row in rows for pid in (row.player_id, row.assist_player_id, row.player_in_id, row.player_out_id) if pid}
    players = _players_by_id(session, player_ids)

    return [
        MatchEvent(
            id=row.id,
            match_id=row.match_id,
            minute=row.minute,
            stoppage_minute=row.stoppage_minute,
            type=row.type,
            team_id=row.team_id,
            player=players.get(row.player_id) if row.player_id else None,
            assist_player=players.get(row.assist_player_id) if row.assist_player_id else None,
            player_in=players.get(row.player_in_id) if row.player_in_id else None,
            player_out=players.get(row.player_out_id) if row.player_out_id else None,
        )
        for row in rows
    ]


def _players_by_id(session: Session, player_ids: Sequence[str]) -> Dict[str, Player]:
    if not player_ids:
        return {}
    rows = session.exec(select(PlayerRow).where(PlayerRow.id.in_(set(player_ids)))).all()
    return {row.id: _to_player(row) for row in rows}


def _match_lineups(session: Session, match_id: str, home_team_id: str, away_team_id: str) -> Optional[MatchLineups]:
    lineup_rows = session.exec(select(MatchLineupRow).where(MatchLineupRow.match_id == match_id)).all()
    if not lineup_rows:
        return None
    lineups_by_team = {row.team_id: row for row in lineup_rows}

    entry_rows = session.exec(
        select(LineupEntryRow).where(LineupEntryRow.match_id == match_id).order_by(LineupEntryRow.order)
    ).all()
    players = _players_by_id(session, [row.player_id for row in entry_rows])

    def build_side(team_id: str) -> TeamLineup:
        lineup_row = lineups_by_team.get(team_id)
        team_entries = [row for row in entry_rows if row.team_id == team_id]
        starting = [players[row.player_id] for row in team_entries if row.role == "starting"]
        subs = [players[row.player_id] for row in team_entries if row.role == "substitute"]
        return TeamLineup(
            team_id=team_id,
            formation=lineup_row.formation if lineup_row else None,
            starting_xi=starting,
            substitutes=subs,
        )

    return MatchLineups(home=build_side(home_team_id), away=build_side(away_team_id))


def _match_statistics(session: Session, match_id: str) -> Optional[MatchStatistics]:
    row = session.get(MatchStatisticsRow, match_id)
    if row is None:
        return None
    return MatchStatistics(
        home=TeamMatchStatistics(
            possession=row.home_possession,
            shots=row.home_shots,
            shots_on_target=row.home_shots_on_target,
            corners=row.home_corners,
        ),
        away=TeamMatchStatistics(
            possession=row.away_possession,
            shots=row.away_shots,
            shots_on_target=row.away_shots_on_target,
            corners=row.away_corners,
        ),
    )


def _now_iso() -> str:
    """Match JS's `Date.toISOString()` format, same as the seed data uses for timestamps."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def update_match(session: Session, match_id: str, update: MatchUpdate) -> Optional[Match]:
    """Apply a partial live-state update (status/minute/score) to a match. Fields left
    unset on `update` are left unchanged. Returns the full match (as `get_match` does),
    or None if the match doesn't exist."""
    row = session.get(MatchRow, match_id)
    if row is None:
        return None

    changes = update.model_dump(exclude_unset=True)
    if "status" in changes:
        row.status = changes["status"]
    if "minute" in changes:
        row.minute = changes["minute"]
    if "stoppage_minute" in changes:
        row.stoppage_minute = changes["stoppage_minute"]
    if "score" in changes:
        row.home_score = changes["score"]["home"]
        row.away_score = changes["score"]["away"]

    row.last_updated = _now_iso()

    session.add(row)
    session.commit()

    return get_match(session, match_id)


def add_match_event(session: Session, match_id: str, payload: MatchEventCreate) -> Optional[Match]:
    """Record a goal, card, or substitution against a live match. A goal also bumps
    `home_score`/`away_score` for `payload.team_id`. Raises ValueError for a team that
    isn't playing in this match, a missing required player, or an unknown player id.
    Returns the full match, or None if the match doesn't exist."""
    row = session.get(MatchRow, match_id)
    if row is None:
        return None

    if payload.team_id not in (row.home_team_id, row.away_team_id):
        raise ValueError(f"team {payload.team_id!r} is not playing in match {match_id!r}")

    if payload.type == "substitution":
        if not payload.player_in_id or not payload.player_out_id:
            raise ValueError("substitution events require playerInId and playerOutId")
    elif not payload.player_id:
        raise ValueError(f"{payload.type} events require playerId")

    event_count = session.exec(
        select(func.count()).select_from(MatchEventRow).where(MatchEventRow.match_id == match_id)
    ).one()

    session.add(
        MatchEventRow(
            id=f"{match_id}-e{event_count + 1}",
            match_id=match_id,
            minute=payload.minute,
            stoppage_minute=payload.stoppage_minute,
            type=payload.type,
            team_id=payload.team_id,
            player_id=payload.player_id,
            assist_player_id=payload.assist_player_id,
            player_in_id=payload.player_in_id,
            player_out_id=payload.player_out_id,
        )
    )

    if payload.type == "goal":
        if payload.team_id == row.home_team_id:
            row.home_score = (row.home_score or 0) + 1
        else:
            row.away_score = (row.away_score or 0) + 1

    row.last_updated = _now_iso()
    session.add(row)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("one of the referenced player ids doesn't exist") from exc

    return get_match(session, match_id)


def get_match(session: Session, match_id: str) -> Optional[Match]:
    row = session.get(MatchRow, match_id)
    if row is None:
        return None

    teams = _team_summaries(session, [row.home_team_id, row.away_team_id])
    leagues = _league_summaries(session, [row.league_id])
    match = _to_match(row, teams, leagues)

    match.events = _match_events(session, match_id)
    match.lineups = _match_lineups(session, match_id, row.home_team_id, row.away_team_id)
    match.statistics = _match_statistics(session, match_id)
    return match


# --- standings ---------------------------------------------------------------------


@dataclass
class _Accumulator:
    team_id: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    results: List[MatchResultLetter] = field(default_factory=list)


def get_standings(session: Session, league_id: str) -> List[Standing]:
    team_ids = [
        row.team_id
        for row in session.exec(select(TeamCompetitionRow).where(TeamCompetitionRow.league_id == league_id)).all()
    ]
    if not team_ids:
        return []

    table: Dict[str, _Accumulator] = {team_id: _Accumulator(team_id=team_id) for team_id in team_ids}

    finished = session.exec(
        select(MatchRow)
        .where(MatchRow.league_id == league_id, MatchRow.status == "finished")
        .order_by(MatchRow.kickoff)
    ).all()

    for match in finished:
        home = table.get(match.home_team_id)
        away = table.get(match.away_team_id)
        if home is None or away is None or match.home_score is None or match.away_score is None:
            continue

        home.played += 1
        away.played += 1
        home.goals_for += match.home_score
        home.goals_against += match.away_score
        away.goals_for += match.away_score
        away.goals_against += match.home_score

        if match.home_score > match.away_score:
            home.won += 1
            away.lost += 1
            home.results.append("W")
            away.results.append("L")
        elif match.home_score < match.away_score:
            away.won += 1
            home.lost += 1
            home.results.append("L")
            away.results.append("W")
        else:
            home.drawn += 1
            away.drawn += 1
            home.results.append("D")
            away.results.append("D")

    standings = [
        Standing(
            league_id=league_id,
            position=0,
            team_id=row.team_id,
            played=row.played,
            won=row.won,
            drawn=row.drawn,
            lost=row.lost,
            goals_for=row.goals_for,
            goals_against=row.goals_against,
            goal_difference=row.goals_for - row.goals_against,
            points=row.won * 3 + row.drawn,
            form=row.results[-5:] or None,
        )
        for row in table.values()
    ]

    standings.sort(key=lambda s: (-s.points, -s.goal_difference, -s.goals_for))
    for idx, row in enumerate(standings):
        row.position = idx + 1

    return standings
