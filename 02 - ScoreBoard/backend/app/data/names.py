from typing import List

from app.models import Player, PlayerPosition

from .rng import seeded_random

FIRST_NAMES = [
    "James", "Lucas", "Mateo", "Noah", "Liam", "Kai", "Diego", "Marco",
    "Leon", "Theo", "Hugo", "Nico", "Omar", "Ivan", "Bruno", "Enzo",
    "Kwame", "Idris", "Rafael", "Tomas", "Sami", "Adrian", "Felix", "Miles",
]

LAST_NAMES = [
    "Silva", "Garcia", "Mendes", "Rossi", "Novak", "Weber", "Dubois", "Kane",
    "Nilsen", "Costa", "Reis", "Haas", "Moreau", "Petit", "Larsen", "Fischer",
    "Okafor", "Traore", "Sakamoto", "Ferreira", "Almeida", "Bianchi", "Schmidt", "Roy",
]

# Starting XI (11) followed by substitutes (7), mirroring the frontend's mock squad shape.
POSITION_TEMPLATE: List[PlayerPosition] = (
    ["GK"]
    + ["DF"] * 4
    + ["MF"] * 4
    + ["FW"] * 2
    + ["GK"]
    + ["DF"] * 2
    + ["MF"] * 2
    + ["FW"] * 2
)


def generate_squad(team_id: str) -> List[Player]:
    """Deterministic 18-player squad for a team, seeded from its id."""
    rng = seeded_random(f"squad:{team_id}")
    used_numbers = set()
    squad: List[Player] = []

    for i, position in enumerate(POSITION_TEMPLATE):
        shirt_number = 1 if i == 0 else int(rng() * 32) + 2
        while shirt_number in used_numbers:
            shirt_number = int(rng() * 32) + 2
        used_numbers.add(shirt_number)

        first = FIRST_NAMES[int(rng() * len(FIRST_NAMES))]
        last = LAST_NAMES[int(rng() * len(LAST_NAMES))]
        squad.append(
            Player(
                id=f"{team_id}-p{i + 1}",
                name=f"{first} {last}",
                shirt_number=shirt_number,
                position=position,
            )
        )
    return squad


def starting_xi(squad: List[Player]) -> List[Player]:
    return squad[:11]


def substitutes(squad: List[Player]) -> List[Player]:
    return squad[11:]
