"use client";

import type { Match } from "@/types";
import { useFollowedTeamIds } from "@/lib/preferences/followed-teams";
import { EmptyState } from "@/components/ui/EmptyState";
import { MatchCard } from "./MatchCard";

export function MatchList({
  matches,
  emptyTitle = "No matches",
  emptyDescription,
}: {
  matches: Match[];
  emptyTitle?: string;
  emptyDescription?: string;
}) {
  const followedTeamIds = useFollowedTeamIds();

  if (matches.length === 0) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
      {matches.map((match) => (
        <MatchCard key={match.id} match={match} followedTeamIds={followedTeamIds} />
      ))}
    </div>
  );
}
