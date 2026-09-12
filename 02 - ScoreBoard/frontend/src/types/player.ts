export type PlayerPosition =
  | "GK"
  | "DF"
  | "MF"
  | "FW";

export interface Player {
  id: string;
  name: string;
  shirtNumber: number;
  position: PlayerPosition;
  countryCode?: string;
}
