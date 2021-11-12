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
    for rnd in tournament.rounds:
        for result in rnd.pairing:
            mapping[result.white] = mapping[result.white] + result.result
            if result.black != BYE:
                mapping[result.black] = mapping[result.black] + 1 - result.result

    return mapping


def player_color_map(tournament: Tournament) -> Dict[Player, tuple[int, int]]:
    mapping: Dict[Player, tuple[int, int]] = {}
    for player in tournament.players:
        mapping[player] = (0, 0)
    mapping[BYE] = (0, 0)
    for rnd in tournament.rounds:
        for result in rnd.pairing:
            if result.black != BYE:
                mapping[result.white] = (mapping[result.white][0] + 1, mapping[result.white][1])
                mapping[result.black] = (mapping[result.black][0], mapping[result.black][1] + 1)

    return mapping
