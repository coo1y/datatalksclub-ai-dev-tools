import type { Match } from "@/types";
import { EmptyState } from "@/components/ui/EmptyState";

interface StatRowProps {
  label: string;
  home: number;
  away: number;
  suffix?: string;
}

/**
 * One entry per line here is all it takes to support an advanced stat
 * (xG, passes, tackles, ...) later — Statistics itself needs no changes.
 */
function StatRow({ label, home, away, suffix = "" }: StatRowProps) {
  const total = home + away || 1;
  const homePct = (home / total) * 100;

  return (
    <div className="mb-4 last:mb-0">
      <div className="mb-1.5 flex items-center justify-between text-sm">
        <span className="font-semibold tabular-nums text-fg">
          {home}
          {suffix}
        </span>
        <span className="text-fg-muted">{label}</span>
        <span className="font-semibold tabular-nums text-fg">
          {away}
          {suffix}
        </span>
      </div>
      <div className="flex h-1.5 overflow-hidden rounded-full bg-surface-2">
        <div className="bg-accent" style={{ width: `${homePct}%` }} />
        <div className="bg-border-strong" style={{ width: `${100 - homePct}%` }} />
      </div>
    </div>
  );
}

export function Statistics({ match }: { match: Match }) {
  if (!match.statistics) {
    return (
      <EmptyState
        title="Statistics not available"
        description="Basic match stats appear once the match kicks off."
      />
    );
  }

  const { home, away } = match.statistics;

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <StatRow label="Possession" home={home.possession} away={away.possession} suffix="%" />
      <StatRow label="Shots" home={home.shots} away={away.shots} />
      <StatRow label="Shots on Target" home={home.shotsOnTarget} away={away.shotsOnTarget} />
      <StatRow label="Corners" home={home.corners} away={away.corners} />
    </div>
  );
}
