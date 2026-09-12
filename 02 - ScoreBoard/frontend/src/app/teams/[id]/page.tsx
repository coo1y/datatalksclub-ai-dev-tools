"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { useMatches } from "@/hooks/useMatches";
import { sortByKickoffAsc, sortByKickoffDesc } from "@/lib/utils/match-sort";
import { TeamHeader } from "@/components/teams/TeamHeader";
import { TeamFixtures } from "@/components/teams/TeamFixtures";
import { TeamResults } from "@/components/teams/TeamResults";
import { StandingsTable } from "@/components/standings/StandingsTable";
import { Section } from "@/components/ui/Section";
import { CardListSkeleton, TableSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";
import { EmptyState } from "@/components/ui/EmptyState";
import type { CompetitionScope } from "@/types";

const SCOPE_LABEL: Record<CompetitionScope, string> = {
  domestic: "Domestic",
  european: "European",
  international: "International",
};

export default function TeamDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: team, status: teamStatus, error: teamError, refetch: refetchTeam } = useAsync(
    () => matchDataProvider.getTeam(id),
    [id],
  );
  const { matches, status: matchesStatus } = useMatches({ teamId: id });
  const { data: leagues } = useAsync(() => matchDataProvider.getLeagues(), []);
  const { data: allTeams } = useAsync(() => matchDataProvider.getTeams(), []);

  const leaguesById = useMemo(
    () => Object.fromEntries((leagues ?? []).map((l) => [l.id, l])),
    [leagues],
  );
  const teamsById = useMemo(
    () => Object.fromEntries((allTeams ?? []).map((t) => [t.id, t])),
    [allTeams],
  );

  const [activeLeagueId, setActiveLeagueId] = useState<string | null>(null);

  useEffect(() => {
    if (team && team.competitions.length > 0 && !activeLeagueId) {
      setActiveLeagueId(team.competitions[0].leagueId);
    }
  }, [team, activeLeagueId]);

  const { data: standings, status: standingsStatus } = useAsync(
    () => (activeLeagueId ? matchDataProvider.getStandings(activeLeagueId) : Promise.resolve([])),
    [activeLeagueId],
  );

  const { fixtures, results } = useMemo(() => {
    if (!matches || !activeLeagueId) return { fixtures: [], results: [] };
    const inCompetition = matches.filter((m) => m.league.id === activeLeagueId);
    return {
      fixtures: sortByKickoffAsc(inCompetition.filter((m) => m.status === "scheduled")),
      results: sortByKickoffDesc(inCompetition.filter((m) => m.status === "finished")),
    };
  }, [matches, activeLeagueId]);

  return (
    <div>
      <Link
        href="/teams"
        className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-fg-muted transition-colors hover:text-fg"
      >
        <ChevronLeft size={16} />
        All teams
      </Link>

      {teamStatus === "loading" ? <CardListSkeleton count={2} /> : null}

      {teamStatus === "error" ? (
        <ErrorState title="Team not found" description={teamError?.message} onRetry={refetchTeam} />
      ) : null}

      {teamStatus === "success" && team ? (
        <>
          <TeamHeader team={team} />

          {team.competitions.length > 1 ? (
            <div className="mb-5 flex gap-1 border-b border-border">
              {team.competitions.map((comp) => (
                <button
                  key={comp.leagueId}
                  onClick={() => setActiveLeagueId(comp.leagueId)}
                  className={`border-b-2 px-3 py-2 text-sm font-medium transition-colors ${
                    activeLeagueId === comp.leagueId
                      ? "border-accent text-fg"
                      : "border-transparent text-fg-muted hover:text-fg"
                  }`}
                >
                  {SCOPE_LABEL[comp.scope]}
                  <span className="ml-1.5 hidden text-xs text-fg-faint sm:inline">
                    {leaguesById[comp.leagueId]?.shortName}
                  </span>
                </button>
              ))}
            </div>
          ) : null}

          {matchesStatus === "loading" ? <CardListSkeleton count={4} /> : null}

          {matchesStatus === "success" && activeLeagueId ? (
            <>
              <Section title="Fixtures" subtitle={leaguesById[activeLeagueId]?.season}>
                <TeamFixtures matches={fixtures} />
              </Section>

              <Section title="Results">
                <TeamResults matches={results} />
              </Section>

              <Section title="League Standings">
                {standingsStatus === "loading" ? <TableSkeleton rows={6} /> : null}
                {standingsStatus === "success" &&
                  (standings && standings.length > 0 ? (
                    <StandingsTable standings={standings} teamsById={teamsById} highlightTeamId={team.id} />
                  ) : (
                    <EmptyState
                      title="Standings not available"
                      description="This competition doesn't publish a league table."
                    />
                  ))}
              </Section>
            </>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
