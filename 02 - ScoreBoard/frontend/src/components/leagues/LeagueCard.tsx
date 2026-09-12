import Link from "next/link";
import type { League } from "@/types";
import { colorForId } from "@/lib/utils/colors";

const SCOPE_LABEL: Record<League["scope"], string> = {
  domestic: "Domestic",
  european: "European",
  international: "International",
};

function LeagueBadge({ league }: { league: League }) {
  return (
    <span
      className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-sm font-bold text-white"
      style={{ backgroundColor: colorForId(league.id) }}
    >
      {league.shortName.slice(0, 2).toUpperCase()}
    </span>
  );
}

export function LeagueCard({ league }: { league: League }) {
  const content = (
    <div
      className={`flex items-center gap-3 rounded-xl border p-4 transition-colors ${
        league.isSupported
          ? "border-border bg-surface hover:border-border-strong hover:bg-surface-hover"
          : "border-border/60 bg-surface/50"
      }`}
    >
      <LeagueBadge league={league} />
      <div className="min-w-0 flex-1">
        <p className={`truncate text-sm font-semibold ${league.isSupported ? "text-fg" : "text-fg-muted"}`}>
          {league.name}
        </p>
        <p className="mt-0.5 truncate text-xs text-fg-muted">
          {league.country} · {SCOPE_LABEL[league.scope]}
        </p>
      </div>
      {league.isSupported ? (
        <span className="shrink-0 rounded-full bg-accent-soft px-2 py-1 text-[11px] font-medium text-accent">
          {league.season}
        </span>
      ) : (
        <span className="shrink-0 rounded-full bg-surface-2 px-2 py-1 text-[11px] font-medium text-fg-faint">
          Coming soon
        </span>
      )}
    </div>
  );

  if (!league.isSupported) {
    return (
      <div aria-disabled="true" className="cursor-not-allowed opacity-80">
        {content}
      </div>
    );
  }

  return (
    <Link href={`/leagues/${league.id}`} className="block">
      {content}
    </Link>
  );
}
