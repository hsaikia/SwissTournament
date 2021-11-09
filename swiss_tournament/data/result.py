from dataclasses import dataclass

from swiss_tournament.data.player import Player


@dataclass
class Result:
    white: Player
    black: Player
    result: float
