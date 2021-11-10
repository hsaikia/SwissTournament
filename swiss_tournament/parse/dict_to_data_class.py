from typing import List

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament


class DictToRoundPairing:
    @staticmethod
    def parse(document: dict) -> List[RoundPairing]:
        if document is None:
            return []
        rounds = []
        for round_name in document.keys():
            rnd = []
            pairing = document[round_name]
            for result in pairing:
                rnd.append(Result(Player(result['w']), Player(result['b']), result['r']))
            rounds.append(RoundPairing(round_name, rnd))
        return rounds


class DictToTournament:
    @staticmethod
    def parse(document: dict) -> Tournament:
        tournament = Tournament(players=[], rounds=[])
        for name in document['players']:
            tournament.players.append(Player(name))
        tournament.rounds = DictToRoundPairing.parse(document['rounds'])
        return tournament
