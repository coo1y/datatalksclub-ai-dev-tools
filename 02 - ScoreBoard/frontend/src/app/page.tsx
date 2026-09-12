"use client";

import { useMemo } from "react";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { useMatches } from "@/hooks/useMatches";
import { useFollowedTeamIds } from "@/lib/preferences/followed-teams";
import { isSameLocalDay, isWithinPastHours } from "@/lib/utils/datetime";
import { pinFollowedFirst, sortByKickoffAsc, sortByKickoffDesc } from "@/lib/utils/match-sort";
import { Section } from "@/components/ui/Section";
import { MatchList } from "@/components/matches/MatchList";
import { CardListSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";

const UPCOMING_WINDOW_DAYS = 7;
const UPCOMING_LIMIT = 9;
const POPULAR_LIMIT = 6;

export default function HomePage() {
  const { matches, status, error, refetch } = useMatches();
  const followedTeamIds = useFollowedTeamIds();
  const { data: teams } = useAsync(() => matchDataProvider.getTeams(), []);

  const popularTeamIds = useMemo(
    () => new Set((teams ?? []).filter((t) => t.isPopular).map((t) => t.id)),
    [teams],
  );

  const sections = useMemo(() => {
    if (!matches) return null;

    const hasFollows = followedTeamIds.length > 0;
    const now = new Date();

    const live = pinFollowedFirst(
      matches.filter((m) => m.status === "live" || m.status === "halftime"),
      followedTeamIds,
    );

    const upcomingPool = matches.filter((m) => {
      if (m.status !== "scheduled") return false;
      const kickoff = new Date(m.kickoff);
      if (kickoff.getTime() < now.getTime()) return false;
      if (!hasFollows) return isSameLocalDay(m.kickoff, now);
      const windowMs = UPCOMING_WINDOW_DAYS * 24 * 60 * 60 * 1000;
      return kickoff.getTime() - now.getTime() <= windowMs;
    });
    const upcoming = pinFollowedFirst(sortByKickoffAsc(upcomingPool), followedTeamIds).slice(
      0,
      UPCOMING_LIMIT,
    );

    const completedPool = matches.filter((m) => m.status === "finished" && isWithinPastHours(m.kickoff, 24));
    const completed = pinFollowedFirst(sortByKickoffDesc(completedPool), followedTeamIds);

    const shownIds = new Set([...live, ...upcoming, ...completed].map((m) => m.id));
    const popularPool = matches.filter(
      (m) =>
        m.status === "scheduled" &&
        !shownIds.has(m.id) &&
        new Date(m.kickoff).getTime() >= now.getTime() &&
        (popularTeamIds.has(m.homeTeam.id) || popularTeamIds.has(m.awayTeam.id)),
    );
    const popular = sortByKickoffAsc(popularPool).slice(0, POPULAR_LIMIT);

    return { live, upcoming, completed, popular, hasFollows };
  }, [matches, followedTeamIds, popularTeamIds]);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold text-fg">
          {sections?.hasFollows ? "Your Home" : "Today"}
        </h1>
        <p className="mt-1 text-sm text-fg-muted">
          {sections?.hasFollows
            ? "Matches from teams you follow, pinned to the top."
            : "Live, upcoming, and recent matches from around the world."}
        </p>
      </div>

      {status === "loading" ? <CardListSkeleton count={6} /> : null}

      {status === "error" ? (
        <ErrorState
          title="Couldn't load matches"
          description={error?.message}
          onRetry={refetch}
        />
      ) : null}

      {status === "success" && sections ? (
        <>
          {sections.live.length > 0 ? (
            <Section title="Live now" subtitle={`${sections.live.length} in progress`}>
              <MatchList matches={sections.live} />
            </Section>
          ) : null}

          <Section title="Upcoming">
            <MatchList
              matches={sections.upcoming}
              emptyTitle="No upcoming matches"
              emptyDescription="Check back soon — new fixtures are added regularly."
            />
          </Section>

          {sections.completed.length > 0 ? (
            <Section title="Recent results" subtitle="Last 24 hours">
              <MatchList matches={sections.completed} />
            </Section>
          ) : null}

          {sections.popular.length > 0 ? (
            <Section title="Popular matches" subtitle="Big teams to watch">
              <MatchList matches={sections.popular} />
            </Section>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
