"use client";

import { useMemo, useState } from "react";
import { matchDataProvider } from "@/lib/api";
import { useAsync } from "@/hooks/useAsync";
import { LeagueSearch } from "@/components/leagues/LeagueSearch";
import { LeagueCard } from "@/components/leagues/LeagueCard";
import { GridSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";
import { EmptyState } from "@/components/ui/EmptyState";

export default function LeaguesPage() {
  const { data: leagues, status, error, refetch } = useAsync(() => matchDataProvider.getLeagues(), []);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!leagues) return [];
    const q = query.trim().toLowerCase();
    if (!q) return leagues;
    return leagues.filter(
      (l) => l.name.toLowerCase().includes(q) || l.country.toLowerCase().includes(q),
    );
  }, [leagues, query]);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold text-fg">Leagues</h1>
        <p className="mt-1 text-sm text-fg-muted">Browse competitions from around the world.</p>
      </div>

      <LeagueSearch value={query} onChange={setQuery} />

      {status === "loading" ? <GridSkeleton count={8} /> : null}

      {status === "error" ? (
        <ErrorState title="Couldn't load leagues" description={error?.message} onRetry={refetch} />
      ) : null}

      {status === "success" ? (
        filtered.length === 0 ? (
          <EmptyState title="No leagues match your search" description="Try a different competition or country." />
        ) : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {filtered.map((league) => (
              <LeagueCard key={league.id} league={league} />
            ))}
          </div>
        )
      ) : null}
    </div>
  );
}
