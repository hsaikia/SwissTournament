from abc import ABC
from typing import List, Dict

from swiss_tournament.data.player import Player
from swiss_tournament.data.tournament import Tournament
from functools import reduce

from swiss_tournament.step.helper_mappings import player_points_map, player_round_map


def _opponent_points(player_rounds: List[tuple[Player, float]], points_map: Dict[Player, float]) -> List[float]:
    return list(map(lambda res: points_map[res[0]], player_rounds))


class TieBreaker(ABC):
    def get(self, player: Player, tournament: Tournament) -> float:
        pass


class Buchholz(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        points = player_points_map(tournament)
        player_rounds = player_round_map(tournament)[player]
        opponent_points = _opponent_points(player_rounds, points)
        result = sum(opponent_points)
        return result


class MedianBuchholz(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        points = player_points_map(tournament)
        player_rounds = player_round_map(tournament)[player]
        opponent_points = _opponent_points(player_rounds, points)
        filtered_points = sorted(opponent_points)
        if len(opponent_points) < 2:
            return 0
        filtered_points.pop()
        del filtered_points[0]
        result = sum(filtered_points)
        return result


class Progressive(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        pass


class BuchholzMinus1(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        points = player_points_map(tournament)
        player_rounds = player_round_map(tournament)[player]
        opponent_points = _opponent_points(player_rounds, points)
        if len(opponent_points) < 1:
            return 0
        filtered_points = sorted(opponent_points, reverse=True)
        filtered_points.pop()
        result = sum(filtered_points)
        return result


class BuchholzMinus2(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        points = player_points_map(tournament)
        player_rounds = player_round_map(tournament)[player]
        opponent_points = _opponent_points(player_rounds, points)
        if len(opponent_points) < 2:
            return 0
        filtered_points = sorted(opponent_points, reverse=True)
        filtered_points.pop()
        filtered_points.pop()
        result = sum(filtered_points)
        return result
