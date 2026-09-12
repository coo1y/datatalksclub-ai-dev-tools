import { AccountSection } from "@/components/settings/AccountSection";
import { FollowedTeamsSection } from "@/components/settings/FollowedTeamsSection";
import { NotificationPreferences } from "@/components/notifications/NotificationPreferences";
import { AppInfoSection } from "@/components/settings/AppInfoSection";

export default function SettingsPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold text-fg">Settings</h1>
        <p className="mt-1 text-sm text-fg-muted">Manage your account, followed teams, and notifications.</p>
      </div>

      <div className="flex max-w-xl flex-col gap-4">
        <AccountSection />
        <FollowedTeamsSection />
        <NotificationPreferences />
        <AppInfoSection />
      </div>
    </div>
  );
}
