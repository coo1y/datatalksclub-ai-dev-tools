import { colorForId } from "@/lib/utils/colors";

const SIZE_CLASSES: Record<number, string> = {
  20: "h-5 w-5 text-[9px]",
  24: "h-6 w-6 text-[10px]",
  32: "h-8 w-8 text-xs",
  40: "h-10 w-10 text-sm",
  56: "h-14 w-14 text-base",
};

export function TeamCrest({
  teamId,
  name,
  shortName,
  crestUrl,
  size = 32,
}: {
  teamId: string;
  name: string;
  shortName: string;
  crestUrl?: string | null;
  size?: 20 | 24 | 32 | 40 | 56;
}) {
  if (crestUrl) {
    return (
      // eslint-disable-next-line @next/next/no-img-element -- external provider crest URLs aren't known ahead of time for next/image's domain allowlist
      <img
        src={crestUrl}
        alt={`${name} crest`}
        className={`${SIZE_CLASSES[size]} shrink-0 rounded-full object-contain`}
      />
    );
  }

  const initials = shortName.slice(0, 3).toUpperCase();

  return (
    <span
      className={`flex shrink-0 items-center justify-center rounded-full font-bold text-white ${SIZE_CLASSES[size]}`}
      style={{ backgroundColor: colorForId(teamId) }}
      aria-label={`${name} crest`}
      title={name}
    >
      {initials}
    </span>
  );
}
