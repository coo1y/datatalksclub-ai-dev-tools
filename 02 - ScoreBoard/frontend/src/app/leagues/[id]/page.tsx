"use client";

import { useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { useMatches } from "@/hooks/useMatches";
import { sortByKickoffAsc, sortByKickoffDesc } from "@/lib/utils/match-sort";
import { Section } from "@/components/ui/Section";
import { MatchList } from "@/components/matches/MatchList";
import { CardListSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";
import { colorForId } from "@/lib/utils/colors";

export default function LeagueDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: league, status: leagueStatus, error: leagueError, refetch: refetchLeague } = useAsync(
    () => matchDataProvider.getLeague(id),
    [id],
  );
  const { matches, status: matchesStatus } = useMatches({ leagueId: id });

  const { live, upcoming, recent } = useMemo(() => {
    if (!matches) return { live: [], upcoming: [], recent: [] };
    return {
      live: matches.filter((m) => m.status === "live" || m.status === "halftime"),
      upcoming: sortByKickoffAsc(matches.filter((m) => m.status === "scheduled")).slice(0, 12),
      recent: sortByKickoffDesc(matches.filter((m) => m.status === "finished")).slice(0, 8),
    };
  }, [matches]);

  return (
    <div>
      <Link
        href="/leagues"
        className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-fg-muted transition-colors hover:text-fg"
      >
        <ChevronLeft size={16} />
        All leagues
      </Link>

      {leagueStatus === "loading" ? <CardListSkeleton count={2} /> : null}

      {leagueStatus === "error" ? (
        <ErrorState
          title="League not found"
          description={leagueError?.message}
          onRetry={refetchLeague}
        />
      ) : null}

      {leagueStatus === "success" && league ? (
        <>
          <div className="mb-6 flex items-center gap-3">
            <span
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-base font-bold text-white"
              style={{ backgroundColor: colorForId(league.id) }}
            >
              {league.shortName.slice(0, 2).toUpperCase()}
            </span>
            <div>
              <h1 className="text-xl font-bold text-fg">{league.name}</h1>
              <p className="text-sm text-fg-muted">
                {league.country} · {league.season}
              </p>
            </div>
          </div>

          {matchesStatus === "loading" ? <CardListSkeleton count={4} /> : null}

          {matchesStatus === "success" ? (
            <>
              {live.length > 0 ? (
                <Section title="Live now">
                  <MatchList matches={live} />
                </Section>
              ) : null}

              <Section title="Upcoming fixtures">
                <MatchList matches={upcoming} emptyTitle="No upcoming fixtures scheduled" />
              </Section>

              <Section title="Recent results">
                <MatchList matches={recent} emptyTitle="No results yet" />
              </Section>

              <p className="mt-2 text-xs text-fg-faint">
                Full league standings are available from any team&rsquo;s page in this competition.
              </p>
            </>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
