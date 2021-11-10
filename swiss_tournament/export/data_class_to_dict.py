from typing import List

from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament


class TournamentToDict:
    @staticmethod
    def parse(tournament: Tournament) -> dict:
        document = {'players': [], 'rounds': {}}

        for player in tournament.players:
            document['players'].append(player.name)

        for rnd in tournament.rounds:
            round_dict = PairingToDict.parse(rnd)
            document['rounds'] = document['rounds'] | round_dict
        return document


class PairingToDict:
    @staticmethod
    def parse(pairing: RoundPairing) -> dict:
        pairings = []
        for result in pairing.pairing:
            res_dict = {
                'w': result.white.name,
                'b': result.black.name,
                'r': result.result
            }
            pairings.append(res_dict)
        return {pairing.name: pairings}
