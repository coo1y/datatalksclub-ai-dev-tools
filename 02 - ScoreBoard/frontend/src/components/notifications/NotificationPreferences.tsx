"use client";

import { useEffect, useState } from "react";
import { BellRing } from "lucide-react";
import {
  getBrowserPermissionState,
  requestBrowserNotificationPermission,
  setNotificationPreference,
  useNotificationPreferences,
  type BrowserPermissionState,
} from "@/lib/notifications/preferences-store";
import { pushNotification } from "@/lib/notifications/notification-center";
import { Switch } from "@/components/ui/Switch";

const PERMISSION_COPY: Record<BrowserPermissionState, string> = {
  unsupported: "Your browser doesn't support notifications — in-app alerts will still work.",
  default: "Browser notifications need your permission to show outside the app.",
  granted: "Browser notifications are enabled.",
  denied: "Browser notifications are blocked. Enable them in your browser settings to receive alerts outside the app.",
};

export function NotificationPreferences() {
  const preferences = useNotificationPreferences();
  const [permission, setPermission] = useState<BrowserPermissionState | null>(null);

  useEffect(() => {
    setPermission(getBrowserPermissionState());
  }, []);

  const requestPermission = async () => {
    const result = await requestBrowserNotificationPermission();
    setPermission(result);
  };

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <h2 className="mb-1 text-sm font-semibold text-fg">Notifications</h2>
      <p className="mb-4 text-xs text-fg-muted">Choose what you want to hear about. Behavior is simulated in this MVP.</p>

      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-fg">Match starts</p>
            <p className="text-xs text-fg-muted">Get notified when a followed team&rsquo;s match kicks off.</p>
          </div>
          <Switch
            checked={preferences.matchStart}
            onChange={(checked) => setNotificationPreference("matchStart", checked)}
            label="Match start notifications"
          />
        </div>

        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-fg">Goals</p>
            <p className="text-xs text-fg-muted">Get notified when a followed team scores.</p>
          </div>
          <Switch
            checked={preferences.goals}
            onChange={(checked) => setNotificationPreference("goals", checked)}
            label="Goal notifications"
          />
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-2 rounded-lg bg-surface-2 p-3">
        <div className="flex items-center gap-2 text-xs text-fg-muted">
          <BellRing size={14} className="shrink-0" />
          <span>{permission ? PERMISSION_COPY[permission] : "Checking browser permission…"}</span>
        </div>
        {permission === "default" ? (
          <button
            onClick={requestPermission}
            className="self-start rounded-md border border-border-strong px-3 py-1.5 text-xs font-medium text-fg transition-colors hover:bg-surface"
          >
            Enable browser notifications
          </button>
        ) : null}
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <button
          onClick={() =>
            pushNotification("match_start", "Arsenal vs Chelsea", "Match starting now")
          }
          className="rounded-md border border-border-strong px-3 py-1.5 text-xs font-medium text-fg transition-colors hover:bg-surface-2"
        >
          Preview match-start alert
        </button>
        <button
          onClick={() =>
            pushNotification("goal", "GOAL — Arsenal 2–1 Chelsea", "67' Player Name")
          }
          className="rounded-md border border-border-strong px-3 py-1.5 text-xs font-medium text-fg transition-colors hover:bg-surface-2"
        >
          Preview goal alert
        </button>
      </div>
    </div>
  );
}
