from typing import Dict, List

import networkx as nx

from swiss_tournament.data.player import BYE, Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.helper_mappings import player_points_map, player_color_map

NEG_INF = -100000000


class RoundGenerator:

    @staticmethod
    def pairing_cost(
            a: Player,
            b: Player,
            player_scores: Dict[Player, float],
            player_colors: Dict[Player, tuple[int, int]]
    ) -> float:
        const = 100
        a_score = player_scores.get(a) or 0
        b_score = player_scores.get(b) or 0
        a_whites, a_blacks = player_colors.get(a) or (0, 0)
        b_whites, b_blacks = player_colors.get(b) or (0, 0)
        score_diff = abs(a_score - b_score)
        color_diff = abs(a_whites - b_blacks) + abs(a_blacks - b_whites)
        if a == BYE:
            return - (const * 20 * b_score)
        elif b == BYE:
            return - (const * 20 * a_score)
        else:
            return -(const * score_diff + color_diff)

    def _populate_graph(
            self,
            tournament: Tournament,
            player_scores: Dict[Player, float],
            player_colors: Dict[Player, tuple[int, int]]
    ) -> nx.Graph:
        graph = nx.Graph()
        graph.clear()

        players = tournament.players
        # One BYE in case we don't have even players
        if len(players) % 2 != 0:
            players.append(BYE)

        # One node per player
        for player in players:
            graph.add_node(player)

        # One edge for each possible match
        for a in players:
            for b in players:
                if a != b:
                    graph.add_edge(a, b, weight=RoundGenerator.pairing_cost(a, b, player_scores, player_colors))

        # Eliminate the option to repeat pairings
        for played_round in tournament.rounds:
            for result in played_round.pairing:
                graph.remove_edge(result.white, result.black)

        return graph

    def _order_weight(self, result: Result, player_scores: Dict[Player, float]):
        if result.black == BYE:
            return -1
        else:
            return player_scores.get(result.white) + player_scores.get(result.black)

    def generate(self, tournament: Tournament) -> List[Result]:
        player_scores = player_points_map(tournament)
        player_colors = player_color_map(tournament)
        graph = self._populate_graph(tournament, player_scores, player_colors)
        pairings = nx.algorithms.matching.max_weight_matching(graph, maxcardinality=True)

        result_pairing: List[Result] = []
        for pairing in pairings:
            a, b = pairing
            a_whites, a_blacks = player_colors[a]
            b_whites, b_blacks = player_colors[b]
            if a == BYE:
                white, black = b, a
            elif b == BYE:
                white, black = a, b
            elif a_whites > b_whites:
                white, black = b, a
            elif a_blacks > b_blacks:
                white, black = a, b
            else:
                white, black = b, a
            result_pairing.append(Result(white, black, None))

        return (sorted(result_pairing,
                       key=lambda result: self._order_weight(result, player_scores),
                       reverse=True))
