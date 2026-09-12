import type { MatchEvent as MatchEventData, MatchEventType } from "@/types";

const EVENT_META: Record<MatchEventType, { icon: string; label: string }> = {
  goal: { icon: "⚽", label: "Goal" },
  yellow_card: { icon: "🟨", label: "Yellow Card" },
  red_card: { icon: "🟥", label: "Red Card" },
  substitution: { icon: "🔁", label: "Substitution" },
};

function eventDetail(event: MatchEventData, teamName: string): string {
  if (event.type === "goal") {
    const assist = event.assistPlayer ? ` (assist: ${event.assistPlayer.name})` : "";
    return `${teamName} — ${event.player?.name ?? "Unknown"}${assist}`;
  }
  if (event.type === "substitution") {
    return `${teamName} — ${event.playerOut?.name ?? "?"} → ${event.playerIn?.name ?? "?"}`;
  }
  return `${teamName} — ${event.player?.name ?? "Unknown"}`;
}

export function MatchEventRow({ event, teamName }: { event: MatchEventData; teamName: string }) {
  const meta = EVENT_META[event.type];
  return (
    <div className="flex gap-3 py-2.5">
      <div className="w-11 shrink-0 pt-0.5 text-right text-xs font-semibold tabular-nums text-fg-muted">
        {event.minute}&rsquo;
        {event.stoppageMinute ? `+${event.stoppageMinute}` : ""}
      </div>
      <div>
        <div className="flex items-center gap-1.5 text-sm font-medium text-fg">
          <span aria-hidden>{meta.icon}</span>
          {meta.label}
        </div>
        <p className="mt-0.5 text-sm text-fg-muted">{eventDetail(event, teamName)}</p>
      </div>
    </div>
  );
}
