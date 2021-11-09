from typing import List

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result


class Tournament:
    players: List[Player]
    rounds: List[Result]
