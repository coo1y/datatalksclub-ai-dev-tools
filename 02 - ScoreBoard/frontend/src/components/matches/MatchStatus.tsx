import type { MatchStatus as MatchStatusType } from "@/types";

export function MatchStatus({
  status,
  minute,
  stoppageMinute,
}: {
  status: MatchStatusType;
  minute?: number;
  stoppageMinute?: number;
}) {
  switch (status) {
    case "live":
      return (
        <span className="flex items-center gap-1.5 text-xs font-bold text-live">
          <span className="animate-live-pulse h-1.5 w-1.5 rounded-full bg-live" />
          LIVE {minute ?? 0}&rsquo;{stoppageMinute ? `+${stoppageMinute}` : ""}
        </span>
      );
    case "halftime":
      return <span className="text-xs font-bold text-live">HALF TIME</span>;
    case "finished":
      return <span className="text-xs font-semibold text-fg-muted">FULL TIME</span>;
    case "postponed":
      return <span className="text-xs font-semibold text-warning">POSTPONED</span>;
    case "cancelled":
      return <span className="text-xs font-semibold text-fg-faint">CANCELLED</span>;
    case "scheduled":
    default:
      return null;
  }
}
