from typing import List, Literal, Optional

from .common import CamelModel
from .team import CompetitionScope

MatchResultLetter = Literal["W", "D", "L"]


class League(CamelModel):
    id: str
    name: str
    short_name: str
    country: str
    logo_url: Optional[str] = None
    scope: CompetitionScope
    is_supported: bool
    season: str


class Standing(CamelModel):
    league_id: str
    position: int
    team_id: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    form: Optional[List[MatchResultLetter]] = None
