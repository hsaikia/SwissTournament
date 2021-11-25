import unittest

from swiss_tournament.data.player import Player, BYE
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.round_generator import RoundGenerator


class RoundGeneratorTestCase(unittest.TestCase):
    unit = RoundGenerator()

    def test_generate_first_round_without_bye(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[]
        )
        new_round = self.unit.generate(tournament)
        self.assertEqual(2, len(new_round))
        for pairing in new_round:
            self.assertNotEqual(pairing.white, pairing.black)

    def test_generate_first_round_with_bye(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie")
            ],
            rounds=[]
        )
        new_round = self.unit.generate(tournament)
        self.assertEqual(2, len(new_round))
        for pairing in new_round:
            self.assertNotEqual(pairing.white, pairing.black)
        # Bye should be paired the last
        self.assertEqual(BYE, new_round[-1].black)

        new_round = self.unit.generate(tournament)
        self.assertEqual(2, len(new_round))
        for pairing in new_round:
            self.assertNotEqual(pairing.white, pairing.black)
        # Bye should be paired the last
        self.assertEqual(BYE, new_round[-1].black)

    def test_generate_second_round_with_only_one_possible_pairing(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), BYE, 1)
                ])
            ]
        )
        new_round = self.unit.generate(tournament)
        self.assertEqual(2, len(new_round))
        self.assertEqual(Result(Player("bob"), Player("charlie"), None), new_round[0])
        # Bye should be paired the last
        self.assertEqual(BYE, new_round[-1].black)
