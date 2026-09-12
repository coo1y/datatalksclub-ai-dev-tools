"""Small deterministic PRNG seeded from a string, so the mock dataset is stable across process restarts."""

from typing import Callable, List, TypeVar

T = TypeVar("T")


def seeded_random(seed: str) -> Callable[[], float]:
    state = 0
    for ch in seed:
        state = (state * 31 + ord(ch)) & 0xFFFFFFFF
    if state == 0:
        state = 0x9E3779B9

    def next_float() -> float:
        nonlocal state
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
        return state / 0xFFFFFFFF

    return next_float


def random_int(rng: Callable[[], float], low: int, high: int) -> int:
    """Inclusive [low, high]."""
    return low + int(rng() * (high - low + 1))


def pick(rng: Callable[[], float], items: List[T]) -> T:
    return items[random_int(rng, 0, len(items) - 1)]
