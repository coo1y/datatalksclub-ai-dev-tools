import type { Match } from "@/types";
import { MatchList } from "@/components/matches/MatchList";

export function TeamFixtures({ matches }: { matches: Match[] }) {
  return (
    <MatchList
      matches={matches}
      emptyTitle="No upcoming fixtures"
      emptyDescription="This competition's fixtures haven't been scheduled yet."
    />
  );
}
