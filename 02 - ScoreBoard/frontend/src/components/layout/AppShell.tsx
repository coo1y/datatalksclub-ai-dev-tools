import type { ReactNode } from "react";
import { Header } from "@/components/navigation/Header";
import { SidebarNav } from "@/components/navigation/SidebarNav";
import { NotificationStack } from "@/components/notifications/NotificationStack";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <div className="flex flex-1 flex-col md:grid md:grid-cols-[220px_1fr]">
        <aside className="hidden border-r border-border md:block">
          <div className="sticky top-14">
            <SidebarNav />
          </div>
        </aside>
        <div className="border-b border-border md:hidden">
          <SidebarNav />
        </div>
        <main className="mx-auto w-full max-w-[1400px] flex-1 px-4 py-6 md:px-8 md:py-8">
          {children}
        </main>
      </div>
      <NotificationStack />
    </div>
  );
}
