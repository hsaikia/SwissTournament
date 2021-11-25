from dataclasses import dataclass
from typing import List

from swiss_tournament.data.player import Player


@dataclass
class PlayerStanding:
    player: Player
    points: float
    tie_breakers: List[float]
