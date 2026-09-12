from typing import Literal, Optional

from .common import CamelModel

PlayerPosition = Literal["GK", "DF", "MF", "FW"]


class Player(CamelModel):
    id: str
    name: str
    shirt_number: int
    position: PlayerPosition
    country_code: Optional[str] = None
