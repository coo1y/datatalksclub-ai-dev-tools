"use client";

import { useMemo, useState } from "react";
import { Search } from "lucide-react";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { TeamCard } from "@/components/teams/TeamCard";
import { GridSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";
import { EmptyState } from "@/components/ui/EmptyState";

export default function TeamsPage() {
  const { data: teams, status, error, refetch } = useAsync(() => matchDataProvider.getTeams(), []);
  const { data: leagues } = useAsync(() => matchDataProvider.getLeagues(), []);
  const [query, setQuery] = useState("");
  const [leagueFilter, setLeagueFilter] = useState("all");

  const leaguesById = useMemo(
    () => Object.fromEntries((leagues ?? []).map((l) => [l.id, l])),
    [leagues],
  );

  const browsableLeagues = useMemo(
    () => (leagues ?? []).filter((l) => l.isSupported),
    [leagues],
  );

  const filtered = useMemo(() => {
    if (!teams) return [];
    const q = query.trim().toLowerCase();
    return teams.filter((team) => {
      const matchesLeague =
        leagueFilter === "all" || team.competitions.some((c) => c.leagueId === leagueFilter);
      const matchesQuery =
        q === "" || team.name.toLowerCase().includes(q) || team.shortName.toLowerCase().includes(q);
      return matchesLeague && matchesQuery;
    });
  }, [teams, query, leagueFilter]);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold text-fg">Teams</h1>
        <p className="mt-1 text-sm text-fg-muted">Search teams or browse by league. Follow up to 10.</p>
      </div>

      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative max-w-sm flex-1">
          <Search size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-fg-faint" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search teams..."
            aria-label="Search teams"
            className="w-full rounded-lg border border-border bg-surface py-2 pl-9 pr-3 text-sm text-fg placeholder:text-fg-faint focus:border-border-strong focus:outline-none"
          />
        </div>
        <select
          value={leagueFilter}
          onChange={(e) => setLeagueFilter(e.target.value)}
          aria-label="Filter by league"
          className="w-full max-w-[220px] rounded-lg border border-border bg-surface px-3 py-2 text-sm text-fg focus:border-border-strong focus:outline-none"
        >
          <option value="all">All leagues</option>
          {browsableLeagues.map((league) => (
            <option key={league.id} value={league.id}>
              {league.name}
            </option>
          ))}
        </select>
      </div>

      {status === "loading" ? <GridSkeleton count={9} /> : null}

      {status === "error" ? (
        <ErrorState title="Couldn't load teams" description={error?.message} onRetry={refetch} />
      ) : null}

      {status === "success" ? (
        filtered.length === 0 ? (
          <EmptyState title="No teams match your search" description="Try a different name or league." />
        ) : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {filtered.map((team) => {
              const primaryLeagueId = team.competitions.find((c) => c.scope === "domestic")?.leagueId
                ?? team.competitions[0]?.leagueId;
              return (
                <TeamCard
                  key={team.id}
                  team={team}
                  competitionLabel={leaguesById[primaryLeagueId ?? ""]?.name}
                />
              );
            })}
          </div>
        )
      ) : null}
    </div>
  );
}
