from typing import Dict, List, Literal, Optional

from pydantic import Field

from .common import CamelModel
from .player import Player

MatchStatus = Literal["scheduled", "live", "halftime", "finished", "postponed", "cancelled"]
MatchEventType = Literal["goal", "yellow_card", "red_card", "substitution"]


class TeamSummary(CamelModel):
    id: str
    name: str
    short_name: str
    crest_url: Optional[str] = None


class LeagueSummary(CamelModel):
    id: str
    name: str
    short_name: str


class MatchScore(CamelModel):
    home: Optional[int] = None
    away: Optional[int] = None


class MatchEvent(CamelModel):
    id: str
    match_id: str
    minute: int
    stoppage_minute: Optional[int] = None
    type: MatchEventType
    team_id: str
    player: Optional[Player] = None
    assist_player: Optional[Player] = None
    player_in: Optional[Player] = None
    player_out: Optional[Player] = None


class TeamLineup(CamelModel):
    team_id: str
    formation: Optional[str] = None
    starting_xi: List[Player] = Field(alias="startingXI")
    substitutes: List[Player]


class MatchLineups(CamelModel):
    home: TeamLineup
    away: TeamLineup


class TeamMatchStatistics(CamelModel):
    possession: int
    shots: int
    shots_on_target: int
    corners: int
    advanced: Optional[Dict[str, float]] = None


class MatchStatistics(CamelModel):
    home: TeamMatchStatistics
    away: TeamMatchStatistics


class MatchEventCreate(CamelModel):
    """A new event to record against a live match: a goal (with scorer and optional
    assist), a card, or a substitution. Scoring a goal also bumps `Match.score` for
    `team_id` — the score doesn't need a separate `MatchUpdate` call for that case."""

    minute: int
    stoppage_minute: Optional[int] = None
    type: MatchEventType
    team_id: str
    player_id: Optional[str] = None
    assist_player_id: Optional[str] = None
    player_in_id: Optional[str] = None
    player_out_id: Optional[str] = None


class MatchUpdate(CamelModel):
    """Partial update for a match's live state. Unset fields are left unchanged."""

    status: Optional[MatchStatus] = None
    minute: Optional[int] = None
    stoppage_minute: Optional[int] = None
    score: Optional[MatchScore] = None


class Match(CamelModel):
    id: str
    league: LeagueSummary
    season: str
    round: Optional[str] = None
    kickoff: str
    status: MatchStatus
    minute: Optional[int] = None
    stoppage_minute: Optional[int] = None
    venue: Optional[str] = None
    home_team: TeamSummary
    away_team: TeamSummary
    score: MatchScore
    events: Optional[List[MatchEvent]] = None
    lineups: Optional[MatchLineups] = None
    statistics: Optional[MatchStatistics] = None
    last_updated: Optional[str] = None
    is_stale: Optional[bool] = None
