import type { Team } from "@/types";
import { TeamCrest } from "@/components/ui/TeamCrest";
import { FollowButton } from "./FollowButton";

export function TeamHeader({ team }: { team: Team }) {
  return (
    <div className="mb-6 flex items-center gap-4 rounded-2xl border border-border bg-surface p-5 sm:p-6">
      <TeamCrest teamId={team.id} name={team.name} shortName={team.shortName} crestUrl={team.crestUrl} size={56} />
      <div className="min-w-0 flex-1">
        <h1 className="truncate text-xl font-bold text-fg">{team.name}</h1>
        <p className="mt-0.5 text-sm text-fg-muted">{team.country}</p>
      </div>
      <FollowButton teamId={team.id} />
    </div>
  );
}
