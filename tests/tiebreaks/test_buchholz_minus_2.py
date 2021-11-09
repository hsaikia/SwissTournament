import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.tie_breaker import BuchholzMinus2


class BuchholzMinus2TestCase(unittest.TestCase):
    unit = BuchholzMinus2()

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
                    [
                        Result(Player("alice"), Player("bob"), 1)
                    ]
                ]
            )
        )
        self.assertEqual(0, result)

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
                    [
                        Result(Player("alice"), Player("bob"), 1),
                        Result(Player("charlie"), Player("dave"), 0.5)
                    ],
                    [
                        Result(Player("charlie"), Player("alice"), 1),
                        Result(Player("dave"), Player("bob"), 1)
                    ]
                ]
            )
        )
        self.assertEqual(0, result)

    def test_with_three_rounds(self):
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
                    [
                        Result(Player("alice"), Player("bob"), 1),
                        Result(Player("charlie"), Player("dave"), 1)
                    ],
                    [
                        Result(Player("charlie"), Player("alice"), 1),
                        Result(Player("dave"), Player("bob"), 0.5)
                    ],
                    [
                        Result(Player("alice"), Player("dave"), 1),
                        Result(Player("bob"), Player("charlie"), 0.5)
                    ]
                ]
            )
        )
        self.assertEqual(2.5, result)
