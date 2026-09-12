"use client";

import { Search } from "lucide-react";

export function LeagueSearch({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <div className="relative mb-5 max-w-sm">
      <Search size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-fg-faint" />
      <input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search leagues..."
        aria-label="Search leagues"
        className="w-full rounded-lg border border-border bg-surface py-2 pl-9 pr-3 text-sm text-fg placeholder:text-fg-faint focus:border-border-strong focus:outline-none"
      />
    </div>
  );
}
