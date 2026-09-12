import Link from "next/link";
import type { Match, TeamSummary } from "@/types";
import { TeamCrest } from "@/components/ui/TeamCrest";
import { StaleDataBadge } from "@/components/ui/StaleDataBadge";
import { formatMatchDate, formatMatchTime } from "@/lib/utils/datetime";
import { MatchStatus } from "./MatchStatus";
import { ScoreDisplay } from "./ScoreDisplay";

function TeamRow({ team, highlighted }: { team: TeamSummary; highlighted: boolean }) {
  return (
    <div className="flex min-w-0 items-center gap-2">
      <TeamCrest teamId={team.id} name={team.name} shortName={team.shortName} crestUrl={team.crestUrl} size={24} />
      <span className={`truncate text-sm ${highlighted ? "font-semibold text-fg" : "text-fg"}`}>
        {team.name}
      </span>
    </div>
  );
}

export function MatchCard({
  match,
  followedTeamIds = [],
}: {
  match: Match;
  followedTeamIds?: string[];
}) {
  const isHomeFollowed = followedTeamIds.includes(match.homeTeam.id);
  const isAwayFollowed = followedTeamIds.includes(match.awayTeam.id);
  const isFollowed = isHomeFollowed || isAwayFollowed;

  return (
    <Link
      href={`/match/${match.id}`}
      className={`block rounded-xl border p-3.5 transition-colors ${
        isFollowed
          ? "border-accent/40 bg-accent-soft/30 hover:border-accent/70"
          : "border-border bg-surface hover:border-border-strong hover:bg-surface-hover"
      }`}
    >
      <div className="mb-2.5 flex items-center justify-between gap-2">
        <span className="truncate text-xs font-medium text-fg-muted">{match.league.name}</span>
        <MatchStatus status={match.status} minute={match.minute} stoppageMinute={match.stoppageMinute} />
      </div>

      <div className="grid grid-cols-[1fr_auto] items-center gap-x-3 gap-y-2">
        <TeamRow team={match.homeTeam} highlighted={isHomeFollowed} />
        <ScoreDisplay value={match.score.home} status={match.status} size="sm" />
        <TeamRow team={match.awayTeam} highlighted={isAwayFollowed} />
        <ScoreDisplay value={match.score.away} status={match.status} size="sm" />
      </div>

      <div className="mt-3 flex items-center justify-between gap-2 text-xs text-fg-muted">
        <span>{formatMatchDate(match.kickoff)}</span>
        <span>{formatMatchTime(match.kickoff)}</span>
      </div>

      {match.isStale && match.lastUpdated ? (
        <div className="mt-2.5">
          <StaleDataBadge lastUpdated={match.lastUpdated} />
        </div>
      ) : null}
    </Link>
  );
}
