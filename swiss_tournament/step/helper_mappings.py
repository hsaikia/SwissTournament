from typing import List, Dict

from generate import Player
from swiss_tournament.data.tournament import Tournament


def player_round_map(tournament: Tournament) -> Dict[Player, List[tuple[Player, float]]]:
    mapping: Dict[Player, List[tuple[Player, float]]] = {}
    for player in tournament.players:
        mapping[player] = []
    for rnd in tournament.rounds:
        for result in rnd:
            white = mapping[result.white]
            white.append((result.black, result.result))
            mapping[result.white] = white
            black = mapping[result.black]
            black.append((result.white, result.result))
            mapping[result.black] = black
    return mapping


def player_points_map(tournament: Tournament) -> Dict[Player, float]:
    mapping: Dict[Player, float] = {}
    for player in tournament.players:
        mapping[player] = 0
    for rnd in tournament.rounds:
        for result in rnd:
            mapping[result.white] = mapping[result.white] + result.result
            mapping[result.black] = mapping[result.black] + 1 - result.result
    return mapping
