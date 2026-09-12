import type { ReactNode } from "react";

export function EmptyState({
  title,
  description,
  icon,
  action,
}: {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-border px-6 py-12 text-center">
      {icon ? <div className="mb-1 text-fg-faint">{icon}</div> : null}
      <p className="text-sm font-semibold text-fg">{title}</p>
      {description ? <p className="max-w-sm text-sm text-fg-muted">{description}</p> : null}
      {action ? <div className="mt-2">{action}</div> : null}
    </div>
  );
}
