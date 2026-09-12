from typing import List, Optional, Tuple

Fixture = Tuple[str, str]  # (home_team_id, away_team_id)


def single_round_robin(team_ids: List[str]) -> List[List[Fixture]]:
    """Circle-method scheduler: every team plays every other team exactly once."""
    teams: List[Optional[str]] = list(team_ids)
    if len(teams) % 2 == 1:
        teams.append(None)  # bye
    n = len(teams)

    rounds: List[List[Fixture]] = []
    for round_idx in range(n - 1):
        pairs: List[Fixture] = []
        for i in range(n // 2):
            a, b = teams[i], teams[n - 1 - i]
            if a is None or b is None:
                continue
            home, away = (a, b) if round_idx % 2 == 0 else (b, a)
            pairs.append((home, away))
        rounds.append(pairs)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return rounds


def double_round_robin(team_ids: List[str]) -> List[List[Fixture]]:
    """Each team plays every other team home and away."""
    first_leg = single_round_robin(team_ids)
    second_leg = [[(away, home) for home, away in round_] for round_ in first_leg]
    return first_leg + second_leg
