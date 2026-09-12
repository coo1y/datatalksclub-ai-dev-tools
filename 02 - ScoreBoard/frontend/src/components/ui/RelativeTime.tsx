"use client";

import { useEffect, useState } from "react";

function formatRelative(fromIso: string, now: number): string {
  const diffMs = now - new Date(fromIso).getTime();
  const minutes = Math.max(0, Math.round(diffMs / 60000));
  if (minutes < 1) return "just now";
  if (minutes === 1) return "1 minute ago";
  if (minutes < 60) return `${minutes} minutes ago`;
  const hours = Math.round(minutes / 60);
  if (hours === 1) return "1 hour ago";
  if (hours < 24) return `${hours} hours ago`;
  const days = Math.round(hours / 24);
  return days === 1 ? "1 day ago" : `${days} days ago`;
}

/** Client-only relative timestamp — avoided in SSR since "now" would differ between server and browser. */
export function RelativeTime({ iso }: { iso: string }) {
  const [label, setLabel] = useState<string | null>(null);

  useEffect(() => {
    setLabel(formatRelative(iso, Date.now()));
    const interval = setInterval(() => setLabel(formatRelative(iso, Date.now())), 30000);
    return () => clearInterval(interval);
  }, [iso]);

  return <span suppressHydrationWarning>{label ?? " "}</span>;
}
