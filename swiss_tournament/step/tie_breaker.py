from abc import ABC
from typing import List

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result


class TieBreaker(ABC):
    def get(self, player: Player, results: List[Result]):
        pass


class Bucholz(TieBreaker):
    def get(self, player: Player, results: List[Result]):
        pass


class MedianBucholz(TieBreaker):
    def get(self, player: Player, results: List[Result]):
        pass


class Progressive(TieBreaker):
    def get(self, player: Player, results: List[Result]):
        pass


class BucholzMinus1(TieBreaker):
    def get(self, player: Player, results: List[Result]):
        pass


class BucholzMinus2(TieBreaker):
    def get(self, player: Player, results: List[Result]):
        pass
