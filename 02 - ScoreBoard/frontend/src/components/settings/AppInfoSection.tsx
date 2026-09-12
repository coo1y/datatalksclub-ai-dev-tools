export function AppInfoSection() {
  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <h2 className="mb-3 text-sm font-semibold text-fg">About</h2>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
        <dt className="text-fg-muted">App</dt>
        <dd className="text-fg">Scoreboard</dd>
        <dt className="text-fg-muted">Version</dt>
        <dd className="text-fg">0.1.0 (MVP)</dd>
        <dt className="text-fg-muted">Data source</dt>
        <dd className="text-fg">Mock data — ready to connect a live sports-data provider</dd>
      </dl>
    </div>
  );
}
