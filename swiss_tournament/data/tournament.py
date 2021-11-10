from dataclasses import dataclass
from typing import List

from swiss_tournament.data.player import Player
from swiss_tournament.data.round_pairing import RoundPairing


@dataclass
class Tournament:
    players: List[Player]
    rounds: List[RoundPairing]
