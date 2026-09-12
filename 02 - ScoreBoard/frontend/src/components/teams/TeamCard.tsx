import Link from "next/link";
import type { Team } from "@/types";
import { TeamCrest } from "@/components/ui/TeamCrest";
import { FollowButton } from "./FollowButton";

export function TeamCard({ team, competitionLabel }: { team: Team; competitionLabel?: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-border bg-surface p-4 transition-colors hover:border-border-strong hover:bg-surface-hover">
      <Link href={`/teams/${team.id}`} className="flex min-w-0 flex-1 items-center gap-3">
        <TeamCrest teamId={team.id} name={team.name} shortName={team.shortName} crestUrl={team.crestUrl} size={40} />
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-fg">{team.name}</p>
          <p className="mt-0.5 truncate text-xs text-fg-muted">
            {team.country}
            {competitionLabel ? ` · ${competitionLabel}` : ""}
          </p>
        </div>
      </Link>
      <FollowButton teamId={team.id} size="sm" />
    </div>
  );
}
