import type { Match } from "@/types";
import { EmptyState } from "@/components/ui/EmptyState";
import { MatchEventRow } from "./MatchEvent";

export function MatchTimeline({ match }: { match: Match }) {
  const events = match.events;

  if (!events || events.length === 0) {
    return (
      <EmptyState
        title="No timeline yet"
        description="Goals, cards, and substitutions will appear here once the match is underway."
      />
    );
  }

  const teamNames: Record<string, string> = {
    [match.homeTeam.id]: match.homeTeam.name,
    [match.awayTeam.id]: match.awayTeam.name,
  };

  const chronologicalDesc = [...events].sort((a, b) => b.minute - a.minute);

  return (
    <div className="divide-y divide-border rounded-xl border border-border bg-surface px-4">
      {chronologicalDesc.map((event) => (
        <MatchEventRow key={event.id} event={event} teamName={teamNames[event.teamId] ?? ""} />
      ))}
    </div>
  );
}
