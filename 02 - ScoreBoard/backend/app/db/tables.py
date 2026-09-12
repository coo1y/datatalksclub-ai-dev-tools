"""SQLModel table definitions — the persisted shape of the data, normalized.

Distinct from `app.models`, which are the camelCase Pydantic response shapes the API
returns; `app/db/repository.py` translates between the two.
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class LeagueRow(SQLModel, table=True):
    __tablename__ = "leagues"

    id: str = Field(primary_key=True)
    name: str
    short_name: str
    country: str
    logo_url: Optional[str] = None
    scope: str
    is_supported: bool
    season: str


class TeamRow(SQLModel, table=True):
    __tablename__ = "teams"

    id: str = Field(primary_key=True)
    name: str
    short_name: str
    crest_url: Optional[str] = None
    country: str
    is_popular: bool = False


class TeamCompetitionRow(SQLModel, table=True):
    __tablename__ = "team_competitions"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: str = Field(foreign_key="teams.id", index=True)
    league_id: str = Field(foreign_key="leagues.id", index=True)
    scope: str


class PlayerRow(SQLModel, table=True):
    __tablename__ = "players"

    id: str = Field(primary_key=True)
    team_id: str = Field(foreign_key="teams.id", index=True)
    name: str
    shirt_number: int
    position: str
    country_code: Optional[str] = None


class MatchRow(SQLModel, table=True):
    __tablename__ = "matches"

    id: str = Field(primary_key=True)
    league_id: str = Field(foreign_key="leagues.id", index=True)
    season: str
    round: Optional[str] = None
    # Stored pre-formatted (matching JS `Date.toISOString()`) so the API never has to
    # round-trip through a driver-specific datetime type to get the wire format right.
    kickoff: str
    status: str
    minute: Optional[int] = None
    stoppage_minute: Optional[int] = None
    venue: Optional[str] = None
    home_team_id: str = Field(foreign_key="teams.id", index=True)
    away_team_id: str = Field(foreign_key="teams.id", index=True)
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    last_updated: Optional[str] = None
    is_stale: bool = False


class MatchEventRow(SQLModel, table=True):
    __tablename__ = "match_events"

    id: str = Field(primary_key=True)
    match_id: str = Field(foreign_key="matches.id", index=True)
    minute: int
    stoppage_minute: Optional[int] = None
    type: str
    team_id: str = Field(foreign_key="teams.id")
    player_id: Optional[str] = Field(default=None, foreign_key="players.id")
    assist_player_id: Optional[str] = Field(default=None, foreign_key="players.id")
    player_in_id: Optional[str] = Field(default=None, foreign_key="players.id")
    player_out_id: Optional[str] = Field(default=None, foreign_key="players.id")


class MatchLineupRow(SQLModel, table=True):
    """One row per side (home/away) of a match's lineup."""

    __tablename__ = "match_lineups"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: str = Field(foreign_key="matches.id", index=True)
    team_id: str = Field(foreign_key="teams.id")
    formation: Optional[str] = None


class LineupEntryRow(SQLModel, table=True):
    """A single player's slot within a `MatchLineupRow` (starting XI or substitute)."""

    __tablename__ = "lineup_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: str = Field(foreign_key="matches.id", index=True)
    team_id: str = Field(foreign_key="teams.id")
    player_id: str = Field(foreign_key="players.id")
    role: str  # "starting" | "substitute"
    order: int  # preserves squad order within the role


class MatchStatisticsRow(SQLModel, table=True):
    __tablename__ = "match_statistics"

    match_id: str = Field(foreign_key="matches.id", primary_key=True)
    home_possession: int
    home_shots: int
    home_shots_on_target: int
    home_corners: int
    away_possession: int
    away_shots: int
    away_shots_on_target: int
    away_corners: int
