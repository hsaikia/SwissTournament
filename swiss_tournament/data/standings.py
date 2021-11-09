from dataclasses import dataclass
from typing import List

from swiss_tournament.data.player import Player


@dataclass
class Standings:
    standings: List[Player]
