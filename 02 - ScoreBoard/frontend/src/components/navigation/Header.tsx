"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Settings, CircleUserRound } from "lucide-react";
import { useAuthUser } from "@/lib/auth/auth-store";

export function Header() {
  const pathname = usePathname();
  const user = useAuthUser();

  return (
    <header className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-border bg-bg/95 px-4 backdrop-blur supports-[backdrop-filter]:bg-bg/80 md:px-6">
      <Link href="/" className="flex items-center gap-2 font-semibold tracking-tight">
        <span className="flex h-7 w-7 items-center justify-center rounded-md bg-accent text-[15px] text-bg">
          ⚽
        </span>
        <span className="hidden sm:inline">Scoreboard</span>
      </Link>

      <div className="flex items-center gap-1.5">
        <Link
          href="/settings"
          aria-current={pathname.startsWith("/settings") ? "page" : undefined}
          className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-sm font-medium transition-colors ${
            pathname.startsWith("/settings")
              ? "bg-surface-2 text-fg"
              : "text-fg-muted hover:bg-surface-2 hover:text-fg"
          }`}
        >
          <Settings size={17} />
          <span className="hidden sm:inline">Settings</span>
        </Link>
        <Link
          href="/settings"
          className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-sm font-medium text-fg-muted transition-colors hover:bg-surface-2 hover:text-fg"
        >
          <CircleUserRound size={17} />
          <span className="hidden sm:inline">{user ? user.email : "Sign in"}</span>
        </Link>
      </div>
    </header>
  );
}
