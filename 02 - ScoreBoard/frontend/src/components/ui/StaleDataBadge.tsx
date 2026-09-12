import { WifiOff } from "lucide-react";
import { RelativeTime } from "./RelativeTime";

export function StaleDataBadge({ lastUpdated }: { lastUpdated: string }) {
  return (
    <div className="flex items-center gap-1.5 rounded-md bg-warning/10 px-2 py-1 text-[11px] font-medium text-warning">
      <WifiOff size={12} />
      <span>
        Last updated <RelativeTime iso={lastUpdated} /> · STALE DATA
      </span>
    </div>
  );
}
