"""Loads the deterministic mock dataset (`app/data`) into the database once, on first boot.

`app/data` remains the single source of truth for *generating* realistic football data;
this module is just the one-time bridge that persists it, so the rest of the app can
stop reading Python lists and start reading the database.

Without ORM `relationship()`s configured on the tables (see `tables.py`), SQLAlchemy's
unit-of-work can't infer cross-table insert ordering from plain `Field(foreign_key=...)`
columns alone — it doesn't reliably order two independently-added mapper classes within
a single flush. Postgres enforces the resulting foreign keys immediately and errors;
SQLite (used in tests) doesn't check them by default, so this only surfaces against a
real database. The fix is to seed strictly in dependency order with an explicit
`session.flush()` between each table, rather than relying on flush to sort it out.
"""

from typing import Set

from sqlmodel import Session, select

from app.data import LEAGUES, MATCHES, TEAMS
from app.models import Player

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


def _seed_leagues(session: Session) -> None:
    for league in LEAGUES:
        session.add(
            LeagueRow(
                id=league.id,
                name=league.name,
                short_name=league.short_name,
                country=league.country,
                logo_url=league.logo_url,
                scope=league.scope,
                is_supported=league.is_supported,
                season=league.season,
            )
        )


def _seed_teams(session: Session) -> None:
    for team in TEAMS:
        session.add(
            TeamRow(
                id=team.id,
                name=team.name,
                short_name=team.short_name,
                crest_url=team.crest_url,
                country=team.country,
                is_popular=bool(team.is_popular),
            )
        )


def _seed_team_competitions(session: Session) -> None:
    for team in TEAMS:
        for comp in team.competitions:
            session.add(TeamCompetitionRow(team_id=team.id, league_id=comp.league_id, scope=comp.scope))


def _seed_matches(session: Session) -> None:
    for match in MATCHES:
        session.add(
            MatchRow(
                id=match.id,
                league_id=match.league.id,
                season=match.season,
                round=match.round,
                kickoff=match.kickoff,
                status=match.status,
                minute=match.minute,
                stoppage_minute=match.stoppage_minute,
                venue=match.venue,
                home_team_id=match.home_team.id,
                away_team_id=match.away_team.id,
                home_score=match.score.home,
                away_score=match.score.away,
                last_updated=match.last_updated,
                is_stale=bool(match.is_stale),
            )
        )


def _iter_lineup_players(match) -> list:
    if not match.lineups:
        return []
    return [
        (team_id, player)
        for team_id, lineup in (
            (match.home_team.id, match.lineups.home),
            (match.away_team.id, match.lineups.away),
        )
        for player in [*lineup.starting_xi, *lineup.substitutes]
    ]


def _seed_players(session: Session) -> None:
    seen: Set[str] = set()
    for match in MATCHES:
        for team_id, player in _iter_lineup_players(match):
            if player.id in seen:
                continue
            seen.add(player.id)
            session.add(
                PlayerRow(
                    id=player.id,
                    team_id=team_id,
                    name=player.name,
                    shirt_number=player.shirt_number,
                    position=player.position,
                    country_code=player.country_code,
                )
            )


def _seed_lineups(session: Session) -> None:
    for match in MATCHES:
        if not match.lineups:
            continue
        for team_id, lineup in (
            (match.home_team.id, match.lineups.home),
            (match.away_team.id, match.lineups.away),
        ):
            session.add(MatchLineupRow(match_id=match.id, team_id=team_id, formation=lineup.formation))


def _seed_lineup_entries(session: Session) -> None:
    for match in MATCHES:
        if not match.lineups:
            continue
        for team_id, lineup in (
            (match.home_team.id, match.lineups.home),
            (match.away_team.id, match.lineups.away),
        ):
            for order, player in enumerate(lineup.starting_xi):
                session.add(
                    LineupEntryRow(match_id=match.id, team_id=team_id, player_id=player.id, role="starting", order=order)
                )
            for order, player in enumerate(lineup.substitutes):
                session.add(
                    LineupEntryRow(match_id=match.id, team_id=team_id, player_id=player.id, role="substitute", order=order)
                )


def _seed_events(session: Session) -> None:
    for match in MATCHES:
        if not match.events:
            continue
        for event in match.events:
            session.add(
                MatchEventRow(
                    id=event.id,
                    match_id=event.match_id,
                    minute=event.minute,
                    stoppage_minute=event.stoppage_minute,
                    type=event.type,
                    team_id=event.team_id,
                    player_id=event.player.id if event.player else None,
                    assist_player_id=event.assist_player.id if event.assist_player else None,
                    player_in_id=event.player_in.id if event.player_in else None,
                    player_out_id=event.player_out.id if event.player_out else None,
                )
            )


def _seed_statistics(session: Session) -> None:
    for match in MATCHES:
        if not match.statistics:
            continue
        session.add(
            MatchStatisticsRow(
                match_id=match.id,
                home_possession=match.statistics.home.possession,
                home_shots=match.statistics.home.shots,
                home_shots_on_target=match.statistics.home.shots_on_target,
                home_corners=match.statistics.home.corners,
                away_possession=match.statistics.away.possession,
                away_shots=match.statistics.away.shots,
                away_shots_on_target=match.statistics.away.shots_on_target,
                away_corners=match.statistics.away.corners,
            )
        )


def seed_if_empty(session: Session) -> None:
    if session.exec(select(LeagueRow)).first() is not None:
        return

    for seed_step in (
        _seed_leagues,
        _seed_teams,
        _seed_team_competitions,
        _seed_matches,
        _seed_players,
        _seed_lineups,
        _seed_lineup_entries,
        _seed_events,
        _seed_statistics,
    ):
        seed_step(session)
        session.flush()

    session.commit()
