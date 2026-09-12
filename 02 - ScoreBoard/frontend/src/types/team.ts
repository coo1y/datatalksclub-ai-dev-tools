export type CompetitionScope = "domestic" | "european" | "international";

export interface TeamCompetitionLink {
  leagueId: string;
  scope: CompetitionScope;
}

export interface Team {
  id: string;
  name: string;
  shortName: string;
  crestUrl: string | null;
  country: string;
  /** Leagues/competitions this team currently participates in. */
  competitions: TeamCompetitionLink[];
  /** Whether this team should be surfaced in "popular matches" on Home. */
  isPopular?: boolean;
}
