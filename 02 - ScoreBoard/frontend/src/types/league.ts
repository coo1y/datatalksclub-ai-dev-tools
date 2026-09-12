import type { CompetitionScope } from "./team";

export interface League {
  id: string;
  name: string;
  shortName: string;
  country: string;
  logoUrl: string | null;
  scope: CompetitionScope;
  /** Leagues not yet backed by real data show a "Coming soon" state. */
  isSupported: boolean;
  season: string;
}

export interface Standing {
  leagueId: string;
  position: number;
  teamId: string;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  goalsFor: number;
  goalsAgainst: number;
  goalDifference: number;
  points: number;
  form?: MatchResultLetter[];
}

export type MatchResultLetter = "W" | "D" | "L";
