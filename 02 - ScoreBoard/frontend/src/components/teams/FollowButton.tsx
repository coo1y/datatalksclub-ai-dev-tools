"use client";

import { useState } from "react";
import { Check, Plus } from "lucide-react";
import { followTeam, unfollowTeam, useFollowedTeamIds } from "@/lib/preferences/followed-teams";

export function FollowButton({
  teamId,
  size = "md",
}: {
  teamId: string;
  size?: "sm" | "md";
}) {
  const followedIds = useFollowedTeamIds();
  const isFollowed = followedIds.includes(teamId);
  const [error, setError] = useState<string | null>(null);

  const toggle = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isFollowed) {
      unfollowTeam(teamId);
      setError(null);
      return;
    }
    const result = followTeam(teamId);
    setError(result.ok ? null : result.reason ?? "Unable to follow team.");
  };

  const sizeClasses = size === "sm" ? "px-2.5 py-1 text-xs" : "px-3.5 py-1.5 text-sm";

  return (
    <div>
      <button
        onClick={toggle}
        aria-pressed={isFollowed}
        className={`inline-flex items-center gap-1.5 rounded-full font-medium transition-colors ${sizeClasses} ${
          isFollowed
            ? "bg-accent-soft text-accent hover:bg-accent-soft/70"
            : "border border-border-strong text-fg hover:bg-surface-2"
        }`}
      >
        {isFollowed ? <Check size={14} /> : <Plus size={14} />}
        {isFollowed ? "Following" : "Follow"}
      </button>
      {error ? <p className="mt-1.5 max-w-[220px] text-xs text-danger">{error}</p> : null}
    </div>
  );
}
