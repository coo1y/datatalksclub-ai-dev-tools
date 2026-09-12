import type { MatchStatus } from "@/types";

const SIZE_CLASSES = {
  sm: "text-base",
  md: "text-lg",
  lg: "text-4xl",
};

export function ScoreDisplay({
  value,
  status,
  size = "md",
}: {
  value: number | null;
  status: MatchStatus;
  size?: keyof typeof SIZE_CLASSES;
}) {
  const isDecided = status === "live" || status === "halftime" || status === "finished";

  if (!isDecided) {
    return <span className={`${SIZE_CLASSES[size]} font-semibold text-fg-faint`}>–</span>;
  }

  return <span className={`${SIZE_CLASSES[size]} font-bold tabular-nums text-fg`}>{value ?? 0}</span>;
}
