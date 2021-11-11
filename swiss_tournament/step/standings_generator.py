from typing import List

from swiss_tournament.data.player_standing import PlayerStanding
from swiss_tournament.data.standings import Standings
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.helper_mappings import player_points_map
from swiss_tournament.step.tie_breaker import TieBreaker, player_tie_breakers_map


class StandingsGenerator:

    @staticmethod
    def sorting_function(player: PlayerStanding) -> tuple:
        sorting_factors = [player.points] + player.tie_breakers
        return tuple(sorting_factors)

    def generate(self, tournament: Tournament, tie_breakers: List[TieBreaker]) -> Standings:
        if not tournament.players:
            return Standings("No Players", [], [])

        if not tournament.rounds:
            return Standings(
                round="Initial Standings",
                standings=list(map(lambda p: PlayerStanding(p, 0, []), tournament.players)),
                tie_breakers=[])

        tie_breakers_mapping = player_tie_breakers_map(tournament, tie_breakers)
        tie_breakers_names = list(map(lambda brk: brk.name(), tie_breakers))
        points_mapping = player_points_map(tournament)
        last_round_name = tournament.rounds[-1].name

        player_standings = []
        for player in tournament.players:
            player_tie_breakers = []
            if tie_breakers_mapping != {}:
                player_tie_breakers = tie_breakers_mapping[player]
            player_standing = PlayerStanding(player, points_mapping[player], player_tie_breakers)
            player_standings.append(player_standing)

        sorted_standings = sorted(player_standings, key=StandingsGenerator.sorting_function, reverse=True)

        return Standings(last_round_name, tie_breakers_names, sorted_standings)
