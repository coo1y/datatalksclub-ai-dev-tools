from datetime import datetime, timedelta, timezone
from typing import Callable, List, Optional

from app.models import (
    LeagueSummary,
    Match,
    MatchEvent,
    MatchLineups,
    MatchScore,
    MatchStatistics,
    MatchStatus,
    TeamLineup,
    TeamMatchStatistics,
    TeamSummary,
)

from .leagues import CURRENT_SEASON, get_league_by_id
from .names import generate_squad, starting_xi, substitutes
from .rng import pick, random_int, seeded_random
from .schedule import Fixture, double_round_robin, single_round_robin
from .teams import TEAMS, get_team_by_id

NOW = datetime.now(timezone.utc)


def _hours_from_now(hours: float) -> datetime:
    return NOW + timedelta(hours=hours)


def _days_from_now(days: int, hour_of_day: int = 15) -> datetime:
    d = NOW + timedelta(days=days)
    return d.replace(hour=hour_of_day, minute=0, second=0, microsecond=0)


def _to_iso(dt: datetime) -> str:
    """Match JS's `Date.toISOString()` format (milliseconds, trailing Z) so the frontend's
    `new Date(iso)` parsing behaves identically to what it does against the mock provider."""
    return dt.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _to_summary(team_id: str) -> TeamSummary:
    team = get_team_by_id(team_id)
    if team is None:
        raise ValueError(f"Unknown team id: {team_id}")
    return TeamSummary(id=team.id, name=team.name, short_name=team.short_name, crest_url=team.crest_url)


def _random_goals(rng: Callable[[], float]) -> int:
    r = rng()
    if r < 0.26:
        return 0
    if r < 0.55:
        return 1
    if r < 0.79:
        return 2
    if r < 0.93:
        return 3
    return 4


def _outfield(squad):
    return [p for p in squad if p.position != "GK"]


def _build_events(
    match_id: str,
    home_team_id: str,
    away_team_id: str,
    home_xi,
    away_xi,
    home_subs,
    away_subs,
    home_goals: int,
    away_goals: int,
    max_minute: int,
    rng: Callable[[], float],
) -> List[MatchEvent]:
    events: List[MatchEvent] = []
    counter = 0

    def add_goal(team_id: str, squad) -> None:
        nonlocal counter
        eligible = _outfield(squad)
        scorer = pick(rng, eligible)
        assist_pool = [p for p in eligible if p.id != scorer.id]
        assist_player = pick(rng, assist_pool) if assist_pool and rng() < 0.6 else None
        counter += 1
        events.append(
            MatchEvent(
                id=f"{match_id}-e{counter}",
                match_id=match_id,
                minute=random_int(rng, 1, max(1, max_minute)),
                type="goal",
                team_id=team_id,
                player=scorer,
                assist_player=assist_player,
            )
        )

    for _ in range(home_goals):
        add_goal(home_team_id, home_xi)
    for _ in range(away_goals):
        add_goal(away_team_id, away_xi)

    card_count = random_int(rng, 2, 4)
    for _ in range(card_count):
        is_home = rng() < 0.5
        team_id = home_team_id if is_home else away_team_id
        squad = _outfield(home_xi if is_home else away_xi)
        counter += 1
        events.append(
            MatchEvent(
                id=f"{match_id}-e{counter}",
                match_id=match_id,
                minute=random_int(rng, 5, max(5, max_minute)),
                type="yellow_card" if rng() < 0.85 else "red_card",
                team_id=team_id,
                player=pick(rng, squad),
            )
        )

    if max_minute > 45:
        def add_subs(team_id: str, xi, subs) -> None:
            nonlocal counter
            sub_count = min(len(subs), random_int(rng, 1, 3))
            used_out = set()
            for i in range(sub_count):
                out_pool = [p for p in xi if p.position != "GK" and p.id not in used_out]
                if not out_pool or i >= len(subs):
                    break
                player_out = pick(rng, out_pool)
                used_out.add(player_out.id)
                counter += 1
                events.append(
                    MatchEvent(
                        id=f"{match_id}-e{counter}",
                        match_id=match_id,
                        minute=random_int(rng, 46, max(46, max_minute)),
                        type="substitution",
                        team_id=team_id,
                        player_out=player_out,
                        player_in=subs[i],
                    )
                )

        add_subs(home_team_id, home_xi, home_subs)
        add_subs(away_team_id, away_xi, away_subs)

    return sorted(events, key=lambda e: e.minute)


def _build_statistics(rng: Callable[[], float]) -> MatchStatistics:
    home_possession = 38 + random_int(rng, 0, 24)
    home_shots = random_int(rng, 6, 18)
    away_shots = random_int(rng, 6, 18)
    return MatchStatistics(
        home=TeamMatchStatistics(
            possession=home_possession,
            shots=home_shots,
            shots_on_target=random_int(rng, 1, min(home_shots, 9)),
            corners=random_int(rng, 1, 10),
        ),
        away=TeamMatchStatistics(
            possession=100 - home_possession,
            shots=away_shots,
            shots_on_target=random_int(rng, 1, min(away_shots, 9)),
            corners=random_int(rng, 1, 10),
        ),
    )


def _build_full_details(match_id: str, home_team_id: str, away_team_id: str,
                         home_goals: int, away_goals: int, max_minute: int):
    rng = seeded_random(match_id)
    home_squad = generate_squad(home_team_id)
    away_squad = generate_squad(away_team_id)
    home_xi = starting_xi(home_squad)
    away_xi = starting_xi(away_squad)
    home_subs = substitutes(home_squad)
    away_subs = substitutes(away_squad)

    events = _build_events(
        match_id, home_team_id, away_team_id, home_xi, away_xi, home_subs, away_subs,
        home_goals, away_goals, max_minute, rng,
    )
    lineups = MatchLineups(
        home=TeamLineup(team_id=home_team_id, formation="4-4-2", starting_xi=home_xi, substitutes=home_subs),
        away=TeamLineup(team_id=away_team_id, formation="4-2-3-1", starting_xi=away_xi, substitutes=away_subs),
    )
    return events, lineups, _build_statistics(rng)


def _make_match(
    league_id: str,
    round_num: int,
    fixture: Fixture,
    kickoff: datetime,
    status: MatchStatus,
    *,
    home_goals: Optional[int] = None,
    away_goals: Optional[int] = None,
    minute: Optional[int] = None,
    with_details: bool = False,
) -> Match:
    home_id, away_id = fixture
    match_id = f"{league_id}-r{round_num}-{home_id}-{away_id}"
    rng = seeded_random(f"{match_id}-score")
    league = get_league_by_id(league_id)
    if league is None:
        raise ValueError(f"Unknown league id: {league_id}")

    is_finished = status == "finished"
    is_live = status in ("live", "halftime")
    home_goals = home_goals if home_goals is not None else (_random_goals(rng) if is_finished else 0)
    away_goals = away_goals if away_goals is not None else (_random_goals(rng) if is_finished else 0)

    no_score_yet = status in ("scheduled", "postponed", "cancelled")
    home_team = _to_summary(home_id)
    away_team = _to_summary(away_id)

    match = Match(
        id=match_id,
        league=LeagueSummary(id=league.id, name=league.name, short_name=league.short_name),
        season=CURRENT_SEASON,
        round=f"Matchday {round_num}",
        kickoff=_to_iso(kickoff),
        status=status,
        minute=minute if is_live else None,
        venue=f"{home_team.short_name} Arena",
        home_team=home_team,
        away_team=away_team,
        score=MatchScore(
            home=None if no_score_yet else home_goals,
            away=None if no_score_yet else away_goals,
        ),
    )

    if with_details or is_live:
        events, lineups, statistics = _build_full_details(
            match_id, home_id, away_id, home_goals, away_goals, minute or 90,
        )
        match.events = events
        match.lineups = lineups
        match.statistics = statistics

    return match


def _domestic_team_ids(league_id: str) -> List[str]:
    return [
        team.id
        for team in TEAMS
        if any(c.league_id == league_id and c.scope in ("domestic", "european") for c in team.competitions)
    ]


def _build_league_matches(league_id: str, team_ids: List[str], *, single_leg: bool, current_index: int) -> List[Match]:
    rounds = single_round_robin(team_ids) if single_leg else double_round_robin(team_ids)
    matches: List[Match] = []

    for round_idx, fixtures in enumerate(rounds):
        round_num = round_idx + 1

        if round_idx < current_index:
            kickoff = _days_from_now(-7 * (current_index - round_idx))
            for fixture in fixtures:
                matches.append(_make_match(league_id, round_num, fixture, kickoff, "finished"))
            continue

        if round_idx == current_index:
            kickoff_today = _hours_from_now(-1)
            for i, fixture in enumerate(fixtures):
                if i == 0:
                    matches.append(_make_match(
                        league_id, round_num, fixture, _hours_from_now(-20), "finished", with_details=True,
                    ))
                elif i == 1:
                    matches.append(_make_match(
                        league_id, round_num, fixture, kickoff_today, "live",
                        home_goals=2, away_goals=1, minute=62,
                    ))
                elif i == 2:
                    matches.append(_make_match(league_id, round_num, fixture, _hours_from_now(5), "scheduled"))
                else:
                    matches.append(_make_match(league_id, round_num, fixture, _days_from_now(3), "scheduled"))
            continue

        kickoff = _days_from_now(7 * (round_idx - current_index))
        for fixture in fixtures:
            matches.append(_make_match(league_id, round_num, fixture, kickoff, "scheduled"))

    return matches


def _build_international_friendlies() -> List[Match]:
    fixtures = [
        (1, ("nation-england", "nation-france")),
        (1, ("nation-spain", "nation-germany")),
        (2, ("nation-italy", "nation-england")),
    ]
    return [
        _make_match("intl-friendlies", 1, fixtures[0][1], _days_from_now(6), "scheduled"),
        _make_match("intl-friendlies", 1, fixtures[1][1], _days_from_now(6), "scheduled"),
        _make_match("intl-friendlies", 2, fixtures[2][1], _days_from_now(-30), "finished"),
    ]


DOMESTIC_LEAGUE_IDS = ["epl", "laliga", "seriea", "bundesliga", "ligue1"]

MATCHES: List[Match] = [
    match
    for league_id in DOMESTIC_LEAGUE_IDS
    for match in _build_league_matches(league_id, _domestic_team_ids(league_id), single_leg=False, current_index=10)
] + _build_league_matches("ucl", _domestic_team_ids("ucl"), single_leg=True, current_index=5) \
  + _build_international_friendlies()

_MATCHES_BY_ID = {match.id: match for match in MATCHES}


def get_match_by_id(match_id: str) -> Optional[Match]:
    return _MATCHES_BY_ID.get(match_id)


def get_matches_by_league(league_id: str) -> List[Match]:
    return [m for m in MATCHES if m.league.id == league_id]


def get_matches_by_team(team_id: str) -> List[Match]:
    return [m for m in MATCHES if m.home_team.id == team_id or m.away_team.id == team_id]
