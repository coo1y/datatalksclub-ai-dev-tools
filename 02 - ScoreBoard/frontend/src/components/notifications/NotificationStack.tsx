"use client";

import { useEffect } from "react";
import { X } from "lucide-react";
import { dismissNotification, useNotifications } from "@/lib/notifications/notification-center";

const AUTO_DISMISS_MS = 6000;

export function NotificationStack() {
  const notifications = useNotifications();

  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-0 z-50 flex flex-col items-center gap-2 p-4 sm:items-end">
      {notifications.map((n) => (
        <ToastItem key={n.id} id={n.id} type={n.type} title={n.title} body={n.body} />
      ))}
    </div>
  );
}

function ToastItem({
  id,
  type,
  title,
  body,
}: {
  id: string;
  type: "match_start" | "goal";
  title: string;
  body: string;
}) {
  useEffect(() => {
    const timer = setTimeout(() => dismissNotification(id), AUTO_DISMISS_MS);
    return () => clearTimeout(timer);
  }, [id]);

  return (
    <div className="animate-toast-in pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl border border-border-strong bg-surface-2 p-3.5 shadow-2xl shadow-black/40">
      <span
        className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm ${
          type === "goal" ? "bg-accent-soft text-accent" : "bg-info/15 text-info"
        }`}
      >
        {type === "goal" ? "⚽" : "▶"}
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-xs font-semibold uppercase tracking-wide text-fg-muted">{title}</p>
        <p className="mt-0.5 text-sm font-medium text-fg">{body}</p>
      </div>
      <button
        onClick={() => dismissNotification(id)}
        aria-label="Dismiss notification"
        className="text-fg-faint transition-colors hover:text-fg"
      >
        <X size={16} />
      </button>
    </div>
  );
}
