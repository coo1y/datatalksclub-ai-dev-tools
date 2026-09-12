import type { Match, TeamSummary } from "@/types";
import { TeamCrest } from "@/components/ui/TeamCrest";
import { StaleDataBadge } from "@/components/ui/StaleDataBadge";
import { MatchStatus } from "@/components/matches/MatchStatus";
import { ScoreDisplay } from "@/components/matches/ScoreDisplay";
import { formatMatchDate, formatMatchTime } from "@/lib/utils/datetime";

function TeamBlock({ team, align = "left" }: { team: TeamSummary; align?: "left" | "right" }) {
  return (
    <div
      className={`flex items-center gap-3 ${align === "right" ? "flex-row-reverse text-right" : ""}`}
    >
      <TeamCrest teamId={team.id} name={team.name} shortName={team.shortName} crestUrl={team.crestUrl} size={40} />
      <span className="font-semibold text-fg">{team.name}</span>
    </div>
  );
}

export function MatchHeader({ match }: { match: Match }) {
  return (
    <div className="mb-6 rounded-2xl border border-border bg-surface p-5 sm:p-6">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2 text-xs text-fg-muted">
        <span className="font-medium text-fg">
          {match.league.name}
          {match.round ? ` · ${match.round}` : ""}
        </span>
        <span>
          {formatMatchDate(match.kickoff)} · {formatMatchTime(match.kickoff)}
        </span>
      </div>

      <div className="mb-3 flex justify-center">
        <MatchStatus status={match.status} minute={match.minute} stoppageMinute={match.stoppageMinute} />
      </div>

      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3 sm:gap-6">
        <TeamBlock team={match.homeTeam} />
        <div className="flex items-center gap-3">
          <ScoreDisplay value={match.score.home} status={match.status} size="lg" />
          <span className="text-2xl text-fg-faint">:</span>
          <ScoreDisplay value={match.score.away} status={match.status} size="lg" />
        </div>
        <TeamBlock team={match.awayTeam} align="right" />
      </div>

      {match.isStale && match.lastUpdated ? (
        <div className="mt-4 flex justify-center">
          <StaleDataBadge lastUpdated={match.lastUpdated} />
        </div>
      ) : null}
    </div>
  );
}
