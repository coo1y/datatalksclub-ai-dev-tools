from typing import List, Literal, Optional

from .common import CamelModel

CompetitionScope = Literal["domestic", "european", "international"]


class TeamCompetitionLink(CamelModel):
    league_id: str
    scope: CompetitionScope


class Team(CamelModel):
    id: str
    name: str
    short_name: str
    crest_url: Optional[str] = None
    country: str
    competitions: List[TeamCompetitionLink]
    is_popular: Optional[bool] = None
