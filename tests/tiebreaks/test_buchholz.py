import unittest

from swiss_tournament.data.player import Player, BYE
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.tie_breaker import Buchholz


class BuchholzTestCase(unittest.TestCase):
    unit = Buchholz()

    def test_without_rounds(self):
        result = self.unit.get(Player("alice"), Tournament([Player("alice")], []))
        self.assertEqual(0, result)

    def test_with_one_round(self):
        result = self.unit.get(
            player=Player("bob"),
            tournament=Tournament(
                players=[
                    Player("alice"),
                    Player("bob")
                ],
                rounds=[
                    RoundPairing("Round 2", [
                        Result(Player("alice"), Player("bob"), 1)
                    ])
                ]
            )
        )
        self.assertEqual(1, result)

    def test_with_two_rounds(self):
        result = self.unit.get(
            player=Player("bob"),
            tournament=Tournament(
                players=[
                    Player("alice"),
                    Player("bob"),
                    Player("charlie"),
                    Player("dave")
                ],
                rounds=[
                    RoundPairing("Round 1", [
                        Result(Player("alice"), Player("bob"), 1),
                        Result(Player("charlie"), Player("dave"), 0.5)
                    ]),
                    RoundPairing("Round 2", [
                        Result(Player("charlie"), Player("alice"), 1),
                        Result(Player("dave"), Player("bob"), 0.5)
                    ])
                ]
            )
        )
        self.assertEqual(2, result)

    def test_with_bye_on_player(self):
        result = self.unit.get(
            player=Player("bob"),
            tournament=Tournament(
                players=[
                    Player("alice"),
                    Player("bob"),
                    Player("charlie"),
                    Player("dave")
                ],
                rounds=[
                    RoundPairing("Round 1", [
                        Result(Player("alice"), Player("bob"), 1),
                        Result(Player("charlie"), Player("dave"), 0.5)
                    ]),
                    RoundPairing("Round 2", [
                        Result(Player("charlie"), Player("alice"), 1),
                        Result(Player("bob"), BYE, 0.5)
                    ])
                ]
            )
        )
        self.assertEqual(1, result)

    def test_with_bye_on_opponent(self):
        result = self.unit.get(
            player=Player("bob"),
            tournament=Tournament(
                players=[
                    Player("alice"),
                    Player("bob"),
                    Player("charlie"),
                    Player("dave")
                ],
                rounds=[
                    RoundPairing("Round 1", [
                        Result(Player("alice"), Player("bob"), 1),
                        Result(Player("charlie"), Player("dave"), 0.5)
                    ]),
                    RoundPairing("Round 2", [
                        Result(Player("alice"), BYE, 1),
                        Result(Player("bob"), Player("charlie"), 0.5)
                    ])
                ]
            )
        )
        self.assertEqual(3, result)
