import type { Player } from "./player";
import type { Team } from "./team";

export type MatchStatus =
  | "scheduled"
  | "live"
  | "halftime"
  | "finished"
  | "postponed"
  | "cancelled";

export type MatchEventType =
  | "goal"
  | "yellow_card"
  | "red_card"
  | "substitution";

/** Minimal team/league info embedded directly on a match payload, mirroring how sports-data providers nest refs. */
export type TeamSummary = Pick<Team, "id" | "name" | "shortName" | "crestUrl">;
export interface LeagueSummary {
  id: string;
  name: string;
  shortName: string;
}

export interface MatchScore {
  home: number | null;
  away: number | null;
}

export interface MatchEvent {
  id: string;
  matchId: string;
  minute: number;
  stoppageMinute?: number;
  type: MatchEventType;
  teamId: string;
  /** Scorer, carded player, or player leaving the pitch on a substitution. */
  player?: Player;
  /** Goal assist. */
  assistPlayer?: Player;
  /** Substitution: player entering the pitch. */
  playerIn?: Player;
  /** Substitution: player leaving the pitch. */
  playerOut?: Player;
}

export interface TeamLineup {
  teamId: string;
  formation?: string;
  startingXI: Player[];
  substitutes: Player[];
}

export interface MatchLineups {
  home: TeamLineup;
  away: TeamLineup;
}

export interface TeamMatchStatistics {
  possession: number;
  shots: number;
  shotsOnTarget: number;
  corners: number;
  /** Room for advanced metrics (xG, passes, tackles, ...) without breaking the shape. */
  advanced?: Record<string, number>;
}

export interface MatchStatistics {
  home: TeamMatchStatistics;
  away: TeamMatchStatistics;
}

export interface Match {
  id: string;
  league: LeagueSummary;
  season: string;
  round?: string;
  /** ISO 8601 timestamp in UTC; render using the viewer's local timezone. */
  kickoff: string;
  status: MatchStatus;
  minute?: number;
  stoppageMinute?: number;
  venue?: string;
  homeTeam: TeamSummary;
  awayTeam: TeamSummary;
  score: MatchScore;
  events?: MatchEvent[];
  lineups?: MatchLineups;
  statistics?: MatchStatistics;
  /** Present when the provider connection has degraded and this is cached data. */
  lastUpdated?: string;
  isStale?: boolean;
}
