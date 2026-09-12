from dataclasses import dataclass
from typing import List, Optional

from app.models import CompetitionScope, Team, TeamCompetitionLink


@dataclass
class _RawTeam:
    id: str
    name: str
    short_name: str
    country: str
    league_id: str
    is_popular: bool = False


RAW_TEAMS: List[_RawTeam] = [
    # Premier League
    _RawTeam("arsenal", "Arsenal", "ARS", "England", "epl", True),
    _RawTeam("chelsea", "Chelsea", "CHE", "England", "epl", True),
    _RawTeam("man-city", "Manchester City", "MCI", "England", "epl", True),
    _RawTeam("liverpool", "Liverpool", "LIV", "England", "epl", True),
    _RawTeam("man-united", "Manchester United", "MUN", "England", "epl", True),
    _RawTeam("tottenham", "Tottenham Hotspur", "TOT", "England", "epl"),
    _RawTeam("newcastle", "Newcastle United", "NEW", "England", "epl"),
    _RawTeam("aston-villa", "Aston Villa", "AVL", "England", "epl"),
    # La Liga
    _RawTeam("real-madrid", "Real Madrid", "RMA", "Spain", "laliga", True),
    _RawTeam("barcelona", "Barcelona", "BAR", "Spain", "laliga", True),
    _RawTeam("atletico-madrid", "Atlético Madrid", "ATM", "Spain", "laliga", True),
    _RawTeam("sevilla", "Sevilla", "SEV", "Spain", "laliga"),
    _RawTeam("real-sociedad", "Real Sociedad", "RSO", "Spain", "laliga"),
    _RawTeam("villarreal", "Villarreal", "VIL", "Spain", "laliga"),
    _RawTeam("athletic-club", "Athletic Club", "ATH", "Spain", "laliga"),
    _RawTeam("real-betis", "Real Betis", "BET", "Spain", "laliga"),
    # Serie A
    _RawTeam("inter-milan", "Inter Milan", "INT", "Italy", "seriea", True),
    _RawTeam("ac-milan", "AC Milan", "MIL", "Italy", "seriea", True),
    _RawTeam("juventus", "Juventus", "JUV", "Italy", "seriea", True),
    _RawTeam("napoli", "Napoli", "NAP", "Italy", "seriea"),
    _RawTeam("as-roma", "AS Roma", "ROM", "Italy", "seriea"),
    _RawTeam("lazio", "Lazio", "LAZ", "Italy", "seriea"),
    _RawTeam("atalanta", "Atalanta", "ATA", "Italy", "seriea"),
    _RawTeam("fiorentina", "Fiorentina", "FIO", "Italy", "seriea"),
    # Bundesliga
    _RawTeam("bayern-munich", "Bayern Munich", "FCB", "Germany", "bundesliga", True),
    _RawTeam("dortmund", "Borussia Dortmund", "BVB", "Germany", "bundesliga", True),
    _RawTeam("rb-leipzig", "RB Leipzig", "RBL", "Germany", "bundesliga"),
    _RawTeam("bayer-leverkusen", "Bayer Leverkusen", "B04", "Germany", "bundesliga"),
    _RawTeam("frankfurt", "Eintracht Frankfurt", "SGE", "Germany", "bundesliga"),
    _RawTeam("stuttgart", "VfB Stuttgart", "VFB", "Germany", "bundesliga"),
    _RawTeam("gladbach", "Borussia Mönchengladbach", "BMG", "Germany", "bundesliga"),
    _RawTeam("wolfsburg", "VfL Wolfsburg", "WOB", "Germany", "bundesliga"),
    # Ligue 1
    _RawTeam("psg", "Paris Saint-Germain", "PSG", "France", "ligue1", True),
    _RawTeam("marseille", "Marseille", "OM", "France", "ligue1"),
    _RawTeam("monaco", "Monaco", "ASM", "France", "ligue1"),
    _RawTeam("lyon", "Lyon", "OL", "France", "ligue1"),
    _RawTeam("lille", "Lille", "LOSC", "France", "ligue1"),
    _RawTeam("nice", "Nice", "OGCN", "France", "ligue1"),
    _RawTeam("lens", "Lens", "RCL", "France", "ligue1"),
    _RawTeam("rennes", "Rennes", "SRFC", "France", "ligue1"),
]

# Teams competing in the Champions League this season, in addition to their domestic league.
UCL_TEAM_IDS = {
    "real-madrid", "man-city", "bayern-munich", "psg",
    "barcelona", "inter-milan", "arsenal", "dortmund",
}

NATIONAL_TEAMS: List[_RawTeam] = [
    _RawTeam("nation-england", "England", "ENG", "England", "intl-friendlies"),
    _RawTeam("nation-spain", "Spain", "ESP", "Spain", "intl-friendlies"),
    _RawTeam("nation-france", "France", "FRA", "France", "intl-friendlies"),
    _RawTeam("nation-germany", "Germany", "GER", "Germany", "intl-friendlies"),
    _RawTeam("nation-italy", "Italy", "ITA", "Italy", "intl-friendlies"),
]


def _to_team(raw: _RawTeam) -> Team:
    scope: CompetitionScope = "international" if raw.league_id == "intl-friendlies" else "domestic"
    competitions = [TeamCompetitionLink(league_id=raw.league_id, scope=scope)]
    if raw.id in UCL_TEAM_IDS:
        competitions.append(TeamCompetitionLink(league_id="ucl", scope="european"))

    return Team(
        id=raw.id,
        name=raw.name,
        short_name=raw.short_name,
        crest_url=None,
        country=raw.country,
        competitions=competitions,
        is_popular=raw.is_popular or None,
    )


TEAMS: List[Team] = [_to_team(raw) for raw in [*RAW_TEAMS, *NATIONAL_TEAMS]]

_TEAMS_BY_ID = {team.id: team for team in TEAMS}


def get_team_by_id(team_id: str) -> Optional[Team]:
    return _TEAMS_BY_ID.get(team_id)


def get_teams_by_league(league_id: str) -> List[Team]:
    return [team for team in TEAMS if any(c.league_id == league_id for c in team.competitions)]
