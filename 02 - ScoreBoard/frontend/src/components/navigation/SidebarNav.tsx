"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Trophy, Users } from "lucide-react";
import { PRIMARY_NAV } from "@/lib/navigation";

const ICONS: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  "/": Home,
  "/leagues": Trophy,
  "/teams": Users,
};

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav
      aria-label="Primary"
      className="flex md:flex-col gap-1 md:gap-1 px-2 py-2 md:px-3 md:py-4 overflow-x-auto md:overflow-visible"
    >
      {PRIMARY_NAV.map((item) => {
        const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        const Icon = ICONS[item.href];
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium whitespace-nowrap transition-colors ${
              isActive
                ? "bg-surface-2 text-fg"
                : "text-fg-muted hover:text-fg hover:bg-surface-2"
            }`}
          >
            {Icon ? (
              <Icon size={18} className={isActive ? "text-accent" : "text-fg-faint"} />
            ) : null}
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
