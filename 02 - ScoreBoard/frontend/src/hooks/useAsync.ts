"use client";

import { useCallback, useEffect, useState } from "react";

export type AsyncStatus = "loading" | "success" | "error";

export interface AsyncState<T> {
  data: T | undefined;
  status: AsyncStatus;
  error: Error | undefined;
  refetch: () => void;
}

/**
 * Runs an async fetcher and tracks loading/success/error status. Re-runs
 * whenever a dependency changes. This is the one place pages need to think
 * about the provider's async boundary — everything downstream just renders
 * loading / error / data.
 */
export function useAsync<T>(fetcher: () => Promise<T>, deps: unknown[]): AsyncState<T> {
  const [data, setData] = useState<T>();
  const [status, setStatus] = useState<AsyncStatus>("loading");
  const [error, setError] = useState<Error>();
  const [tick, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setStatus("loading");
    setError(undefined);

    fetcher()
      .then((result) => {
        if (cancelled) return;
        setData(result);
        setStatus("success");
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setError(err instanceof Error ? err : new Error(String(err)));
        setStatus("error");
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, tick]);

  const refetch = useCallback(() => setTick((t) => t + 1), []);

  return { data, status, error, refetch };
}
