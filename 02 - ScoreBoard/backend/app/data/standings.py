from dataclasses import dataclass, field
from typing import Dict, List

from app.models import MatchResultLetter, Standing

from .matches import get_matches_by_league
from .teams import get_teams_by_league

STANDINGS_LEAGUE_IDS = ["epl", "laliga", "seriea", "bundesliga", "ligue1", "ucl"]


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


def _compute_standings_for_league(league_id: str) -> List[Standing]:
    teams = get_teams_by_league(league_id)
    finished = sorted(
        (m for m in get_matches_by_league(league_id) if m.status == "finished"),
        key=lambda m: m.kickoff,
    )

    table: Dict[str, _Accumulator] = {team.id: _Accumulator(team_id=team.id) for team in teams}

    for match in finished:
        home = table.get(match.home_team.id)
        away = table.get(match.away_team.id)
        if home is None or away is None or match.score.home is None or match.score.away is None:
            continue

        home.played += 1
        away.played += 1
        home.goals_for += match.score.home
        home.goals_against += match.score.away
        away.goals_for += match.score.away
        away.goals_against += match.score.home

        if match.score.home > match.score.away:
            home.won += 1
            away.lost += 1
            home.results.append("W")
            away.results.append("L")
        elif match.score.home < match.score.away:
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


STANDINGS: Dict[str, List[Standing]] = {
    league_id: _compute_standings_for_league(league_id) for league_id in STANDINGS_LEAGUE_IDS
}


def get_standings_by_league(league_id: str) -> List[Standing]:
    return STANDINGS.get(league_id, [])
