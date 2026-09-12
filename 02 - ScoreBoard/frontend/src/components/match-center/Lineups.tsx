import type { Match, Player, TeamLineup } from "@/types";
import { EmptyState } from "@/components/ui/EmptyState";

function PlayerRow({ player }: { player: Player }) {
  return (
    <li className="flex items-center gap-2.5 py-1 text-sm text-fg">
      <span className="w-5 shrink-0 text-right text-xs tabular-nums text-fg-faint">{player.shirtNumber}</span>
      <span className="truncate">{player.name}</span>
      <span className="ml-auto shrink-0 text-xs text-fg-faint">{player.position}</span>
    </li>
  );
}

function LineupColumn({ title, lineup }: { title: string; lineup: TeamLineup }) {
  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold text-fg">
        {title}
        {lineup.formation ? <span className="ml-1.5 font-normal text-fg-muted">({lineup.formation})</span> : null}
      </h3>
      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-fg-faint">Starting XI</p>
      <ul className="mb-4">
        {lineup.startingXI.map((player) => (
          <PlayerRow key={player.id} player={player} />
        ))}
      </ul>
      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-fg-faint">Substitutes</p>
      <ul>
        {lineup.substitutes.map((player) => (
          <PlayerRow key={player.id} player={player} />
        ))}
      </ul>
    </div>
  );
}

export function Lineups({ match }: { match: Match }) {
  if (!match.lineups) {
    return (
      <EmptyState
        title="Lineups not available"
        description="Lineups are typically confirmed closer to kickoff."
      />
    );
  }

  return (
    <div className="grid grid-cols-1 gap-8 rounded-xl border border-border bg-surface p-5 sm:grid-cols-2">
      <LineupColumn title={match.homeTeam.name} lineup={match.lineups.home} />
      <LineupColumn title={match.awayTeam.name} lineup={match.lineups.away} />
    </div>
  );
}
