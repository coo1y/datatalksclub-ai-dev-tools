"use client";

import { useEffect, useState } from "react";
import { matchDataProvider } from "@/lib/api";
import type { Match } from "@/types";
import { useAsync } from "./useAsync";

export function useMatch(id: string) {
  const { data, status, error, refetch } = useAsync(() => matchDataProvider.getMatch(id), [id]);
  const [match, setMatch] = useState<Match | undefined>(undefined);

  useEffect(() => {
    setMatch(data);
  }, [data]);

  useEffect(() => {
    const unsubscribe = matchDataProvider.subscribeToMatch(id, (updated) => setMatch(updated));
    return unsubscribe;
  }, [id]);

  return { match, status, error, refetch };
}
