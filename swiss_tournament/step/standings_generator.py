from typing import List

from swiss_tournament.data.standings import Standings
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.tie_breaker import TieBreaker


class StandingsGenerator:
    def generate(self, tournament: Tournament, tie_breakers: List[TieBreaker]) -> Standings:
        pass
