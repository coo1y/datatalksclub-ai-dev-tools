import { AlertTriangle } from "lucide-react";

export function ErrorState({
  title = "Something went wrong",
  description,
  onRetry,
}: {
  title?: string;
  description?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-border bg-surface px-6 py-12 text-center">
      <AlertTriangle size={22} className="mb-1 text-danger" />
      <p className="text-sm font-semibold text-fg">{title}</p>
      {description ? <p className="max-w-sm text-sm text-fg-muted">{description}</p> : null}
      {onRetry ? (
        <button
          onClick={onRetry}
          className="mt-2 rounded-md border border-border-strong px-3 py-1.5 text-sm font-medium text-fg transition-colors hover:bg-surface-2"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}
