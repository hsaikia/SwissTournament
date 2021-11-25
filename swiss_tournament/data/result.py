from dataclasses import dataclass
from typing import Optional

from swiss_tournament.data.player import Player


@dataclass
class Result:
    white: Player
    black: Player
    result: Optional[float]
