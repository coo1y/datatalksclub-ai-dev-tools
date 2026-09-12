"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import { useMatch } from "@/hooks/useMatch";
import { MatchHeader } from "@/components/match-center/MatchHeader";
import { MatchTimeline } from "@/components/match-center/MatchTimeline";
import { Lineups } from "@/components/match-center/Lineups";
import { Statistics } from "@/components/match-center/Statistics";
import { CardListSkeleton } from "@/components/ui/LoadingState";
import { ErrorState } from "@/components/ui/ErrorState";

const TABS = [
  { id: "timeline", label: "Timeline" },
  { id: "lineups", label: "Lineups" },
  { id: "stats", label: "Statistics" },
] as const;

type TabId = (typeof TABS)[number]["id"];

export default function MatchCenterPage() {
  const { id } = useParams<{ id: string }>();
  const { match, status, error, refetch } = useMatch(id);
  const [tab, setTab] = useState<TabId>("timeline");

  return (
    <div>
      <Link
        href="/"
        className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-fg-muted transition-colors hover:text-fg"
      >
        <ChevronLeft size={16} />
        Back to Home
      </Link>

      {status === "loading" ? <CardListSkeleton count={4} /> : null}

      {status === "error" || (status === "success" && !match) ? (
        <ErrorState
          title="Match not found"
          description={error?.message ?? "This match doesn't exist or is no longer available."}
          onRetry={refetch}
        />
      ) : null}

      {status === "success" && match ? (
        <>
          <MatchHeader match={match} />

          <div className="mb-4 flex gap-1 border-b border-border">
            {TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`border-b-2 px-3 py-2 text-sm font-medium transition-colors ${
                  tab === t.id
                    ? "border-accent text-fg"
                    : "border-transparent text-fg-muted hover:text-fg"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {tab === "timeline" ? <MatchTimeline match={match} /> : null}
          {tab === "lineups" ? <Lineups match={match} /> : null}
          {tab === "stats" ? <Statistics match={match} /> : null}
        </>
      ) : null}
    </div>
  );
}
