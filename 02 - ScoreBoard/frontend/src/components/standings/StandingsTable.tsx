import type { Standing, Team } from "@/types";
import { TeamCrest } from "@/components/ui/TeamCrest";

export function StandingsTable({
  standings,
  teamsById,
  highlightTeamId,
}: {
  standings: Standing[];
  teamsById: Record<string, Team>;
  highlightTeamId?: string;
}) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border bg-surface">
      <table className="w-full min-w-[520px] border-collapse text-sm">
        <thead>
          <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-fg-faint">
            <th className="px-3 py-2.5 font-medium">Pos</th>
            <th className="px-3 py-2.5 font-medium">Team</th>
            <th className="px-2 py-2.5 text-center font-medium">P</th>
            <th className="px-2 py-2.5 text-center font-medium">W</th>
            <th className="px-2 py-2.5 text-center font-medium">D</th>
            <th className="px-2 py-2.5 text-center font-medium">L</th>
            <th className="px-2 py-2.5 text-center font-medium">GD</th>
            <th className="px-3 py-2.5 text-center font-medium">Pts</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((row) => {
            const team = teamsById[row.teamId];
            const isHighlighted = row.teamId === highlightTeamId;
            return (
              <tr
                key={row.teamId}
                className={`border-b border-border last:border-0 ${isHighlighted ? "bg-accent-soft/40" : ""}`}
              >
                <td className="px-3 py-2 tabular-nums text-fg-muted">{row.position}</td>
                <td className="px-3 py-2">
                  <div className="flex min-w-0 items-center gap-2">
                    {team ? (
                      <TeamCrest
                        teamId={team.id}
                        name={team.name}
                        shortName={team.shortName}
                        crestUrl={team.crestUrl}
                        size={20}
                      />
                    ) : null}
                    <span className="truncate font-medium text-fg">{team?.name ?? row.teamId}</span>
                  </div>
                </td>
                <td className="px-2 py-2 text-center tabular-nums text-fg-muted">{row.played}</td>
                <td className="px-2 py-2 text-center tabular-nums text-fg-muted">{row.won}</td>
                <td className="px-2 py-2 text-center tabular-nums text-fg-muted">{row.drawn}</td>
                <td className="px-2 py-2 text-center tabular-nums text-fg-muted">{row.lost}</td>
                <td className="px-2 py-2 text-center tabular-nums text-fg-muted">
                  {row.goalDifference > 0 ? "+" : ""}
                  {row.goalDifference}
                </td>
                <td className="px-3 py-2 text-center font-bold tabular-nums text-fg">{row.points}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
