import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.tournament_updater import TournamentUpdater


class TournamentUpdaterTestCase(unittest.TestCase):
    unit = TournamentUpdater()

    def test_update_tournament_with_new_round(self):
        tournament = Tournament(players=[], rounds=[])
        new_round = RoundPairing("New Round", [Result(Player("Alice"), Player("Bob"), 1)])
        self.unit.update(tournament, new_round)
        self.assertEqual(1, len(tournament.rounds))
        self.assertEqual(new_round, tournament.rounds[0])
