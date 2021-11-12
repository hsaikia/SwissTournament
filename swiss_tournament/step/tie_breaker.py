from abc import ABC
from typing import List, Dict

from swiss_tournament.data.player import Player
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.helper_mappings import player_points_map, player_round_map


def _opponent_points(player_rounds: List[tuple[Player, float]], points_map: Dict[Player, float]) -> List[float]:
    return list(map(lambda res: points_map.get(res[0]) or 0, player_rounds))


class TieBreaker(ABC):
    def get(self, player: Player, tournament: Tournament) -> float:
        pass

    def name(self) -> str:
        pass


def player_tie_breakers_map(tournament: Tournament, tie_breakers: List[TieBreaker]) -> Dict[Player, List[float]]:
    mapping = {}
    for player in tournament.players:
        results = []
        for tie_breaker in tie_breakers:
            results.append(tie_breaker.get(player, tournament))
        mapping[player] = results
    return mapping


class Buchholz(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        points = player_points_map(tournament)
        player_rounds = player_round_map(tournament)[player]
        opponent_points = _opponent_points(player_rounds, points)
        result = sum(opponent_points)
        return result

    def name(self):
        return "Buchholz"


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

    def name(self):
        return "Buchholz M"


class Progressive(TieBreaker):
    def get(self, player: Player, tournament: Tournament) -> float:
        player_rounds = player_round_map(tournament)[player]
        round_count = len(player_rounds)
        result = 0
        for i in range(0, round_count):
            round_result = player_rounds[i][1]
            result += round_result * (round_count - i)
        return result

    def name(self):
        return "Progressive"


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

    def name(self):
        return "Buchholz -1"


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

    def name(self):
        return "Buchholz -2"
