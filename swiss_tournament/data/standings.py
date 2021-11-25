from dataclasses import dataclass
from typing import List

from swiss_tournament.data.player_standing import PlayerStanding


@dataclass
class Standings:
    round: str
    tie_breakers: List[str]
    standings: List[PlayerStanding]
