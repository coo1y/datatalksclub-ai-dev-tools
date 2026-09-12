"use client";

import Link from "next/link";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { MAX_FOLLOWED_TEAMS, unfollowTeam, useFollowedTeamIds } from "@/lib/preferences/followed-teams";
import { TeamCrest } from "@/components/ui/TeamCrest";
import { X } from "lucide-react";

export function FollowedTeamsSection() {
  const followedIds = useFollowedTeamIds();
  const { data: teams } = useAsync(() => matchDataProvider.getTeams(), []);
  const followedTeams = (teams ?? []).filter((t) => followedIds.includes(t.id));

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-fg">Followed teams</h2>
        <span className="text-xs text-fg-muted">
          {followedIds.length} / {MAX_FOLLOWED_TEAMS}
        </span>
      </div>

      {followedTeams.length === 0 ? (
        <p className="text-sm text-fg-muted">
          You&rsquo;re not following any teams yet.{" "}
          <Link href="/teams" className="font-medium text-accent hover:underline">
            Browse teams
          </Link>{" "}
          to follow up to {MAX_FOLLOWED_TEAMS}.
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {followedTeams.map((team) => (
            <li
              key={team.id}
              className="flex items-center gap-2.5 rounded-lg border border-border bg-surface-2 px-3 py-2"
            >
              <TeamCrest teamId={team.id} name={team.name} shortName={team.shortName} crestUrl={team.crestUrl} size={24} />
              <Link href={`/teams/${team.id}`} className="flex-1 truncate text-sm font-medium text-fg hover:underline">
                {team.name}
              </Link>
              <button
                onClick={() => unfollowTeam(team.id)}
                aria-label={`Unfollow ${team.name}`}
                className="text-fg-faint transition-colors hover:text-danger"
              >
                <X size={16} />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
