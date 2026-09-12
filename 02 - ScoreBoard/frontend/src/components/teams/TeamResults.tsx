import type { Match } from "@/types";
import { MatchList } from "@/components/matches/MatchList";

export function TeamResults({ matches }: { matches: Match[] }) {
  return (
    <MatchList
      matches={matches}
      emptyTitle="No results yet"
      emptyDescription="Results will appear here once matches have been played."
    />
  );
}
