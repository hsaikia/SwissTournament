from typing import List, Dict

from generate import Player
from swiss_tournament.data.player import BYE
from swiss_tournament.data.tournament import Tournament


def player_round_map(tournament: Tournament) -> Dict[Player, List[tuple[Player, float]]]:
    mapping: Dict[Player, List[tuple[Player, float]]] = {}
    for player in tournament.players:
        mapping[player] = []
    mapping[BYE] = []
    for rnd in tournament.rounds:
        for result in rnd.pairing:
            white = mapping[result.white]
            white.append((result.black, result.result))
            mapping[result.white] = white
            black = mapping[result.black]
            black.append((result.white, 1 - result.result))
            mapping[result.black] = black

    # Remove results from fictional BYE player
    mapping[BYE] = []
    return mapping


def player_points_map(tournament: Tournament) -> Dict[Player, float]:
    mapping: Dict[Player, float] = {}
    for player in tournament.players:
        mapping[player] = 0
    mapping[BYE] = 0
    for rnd in tournament.rounds:
        for result in rnd.pairing:
            mapping[result.white] = mapping[result.white] + result.result
            mapping[result.black] = mapping[result.black] + 1 - result.result

    # Remove results from fictional BYE player
    mapping[BYE] = 0
    return mapping
