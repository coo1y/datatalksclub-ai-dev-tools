"use client";

import { useEffect, useState } from "react";
import { matchDataProvider, type GetMatchesParams } from "@/lib/api";
import type { Match } from "@/types";
import { useAsync } from "./useAsync";

/**
 * Fetches matches once, then keeps live matches ticking via the provider's
 * push-based subscription rather than re-polling the whole list.
 */
export function useMatches(params?: GetMatchesParams) {
  const key = JSON.stringify(params ?? {});
  const { data, status, error, refetch } = useAsync(
    () => matchDataProvider.getMatches(params),
    [key],
  );
  const [matches, setMatches] = useState<Match[] | undefined>(undefined);

  useEffect(() => {
    setMatches(data);
  }, [data]);

  useEffect(() => {
    const unsubscribe = matchDataProvider.subscribeToLiveUpdates((liveMatches) => {
      setMatches((prev) => {
        if (!prev) return prev;
        const liveById = new Map(liveMatches.map((m) => [m.id, m]));
        return prev.map((m) => liveById.get(m.id) ?? m);
      });
    });
    return unsubscribe;
  }, []);

  return { matches, status, error, refetch };
}
