import type { ReactNode } from "react";

export function Section({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section className="mb-9">
      <div className="mb-3 flex items-baseline justify-between gap-2">
        <h2 className="text-base font-semibold text-fg">{title}</h2>
        {subtitle ? <span className="text-xs text-fg-muted">{subtitle}</span> : null}
      </div>
      {children}
    </section>
  );
}
