import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.player_standing import PlayerStanding
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.standings import Standings
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.step.standings_generator import StandingsGenerator
from swiss_tournament.step.tie_breaker import Progressive, Buchholz


class StandingsGeneratorTestCase(unittest.TestCase):
    unit = StandingsGenerator()

    def test_generate_standings_with_no_players(self):
        tournament = Tournament(players=[], rounds=[])
        standings = self.unit.generate(tournament, [])
        self.assertEqual(Standings("No Players", [], []), standings)

    def test_generate_standings_without_rounds(self):
        tournament = Tournament(players=[
            Player("Alice"),
            Player("Bob")
        ], rounds=[])
        standings = self.unit.generate(tournament, [])
        self.assertEqual(
            Standings(
                "Initial Standings",
                [],
                [
                    PlayerStanding(Player("Alice"), 0, []),
                    PlayerStanding(Player("Bob"), 0, [])
                ]
            ), standings)

    def test_generate_standings_without_tie_breakers(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), Player("dave"), 1)
                ]),
                RoundPairing("Round 2", [
                    Result(Player("charlie"), Player("alice"), 1),
                    Result(Player("dave"), Player("bob"), 0.5)
                ]),
                RoundPairing("Round 3", [
                    Result(Player("alice"), Player("dave"), 1),
                    Result(Player("bob"), Player("charlie"), 0.5)
                ])
            ]
        )
        standings = self.unit.generate(tournament, [])
        self.assertEqual(
            Standings(
                "Round 3",
                [],
                [
                    PlayerStanding(Player("charlie"), 2.5, []),
                    PlayerStanding(Player("bob"), 2, []),
                    PlayerStanding(Player("alice"), 1, []),
                    PlayerStanding(Player("dave"), 0.5, [])
                ]
            ), standings)

    def test_generate_standings_with_one_tie_breaker(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), Player("dave"), 1)
                ]),
                RoundPairing("Round 2", [
                    Result(Player("charlie"), Player("alice"), 0),
                    Result(Player("dave"), Player("bob"), 0.5)
                ]),
                RoundPairing("Round 3", [
                    Result(Player("alice"), Player("dave"), 1),
                    Result(Player("bob"), Player("charlie"), 0.5)
                ])
            ]
        )
        standings = self.unit.generate(tournament, [Progressive()])
        self.assertEqual(
            Standings(
                "Round 3",
                ["Progressive"],
                [
                    PlayerStanding(Player("bob"), 2, [4.5]),
                    PlayerStanding(Player("alice"), 2, [3]),
                    PlayerStanding(Player("charlie"), 1.5, [3.5]),
                    PlayerStanding(Player("dave"), 0.5, [1])
                ]
            ), standings)

    def test_generate_standings_with_two_tie_breaker_where_first_is_tied_and_second_decides(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), Player("dave"), 1)
                ]),
                RoundPairing("Round 2", [
                    Result(Player("charlie"), Player("alice"), 0),
                    Result(Player("dave"), Player("bob"), 0.5)
                ]),
                RoundPairing("Round 3", [
                    Result(Player("alice"), Player("dave"), 1),
                    Result(Player("bob"), Player("charlie"), 0.5)
                ])
            ]
        )
        standings = self.unit.generate(tournament, [Buchholz(), Progressive()])
        self.assertEqual(
            Standings(
                "Round 3",
                ["Buchholz", "Progressive"],
                [
                    PlayerStanding(Player("bob"), 2, [4, 4.5]),
                    PlayerStanding(Player("alice"), 2, [4, 3]),
                    PlayerStanding(Player("charlie"), 1.5, [4.5, 3.5]),
                    PlayerStanding(Player("dave"), 0.5, [5.5, 1])
                ]
            ), standings)

    def test_generate_standings_with_two_tie_breaker_where_first_decides_being_buchholz(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), Player("dave"), 1)
                ]),
                RoundPairing("Round 2", [
                    Result(Player("charlie"), Player("alice"), 0),
                    Result(Player("dave"), Player("bob"), 0.5)
                ])
            ]
        )
        standings = self.unit.generate(tournament, [Buchholz(), Progressive()])
        self.assertEqual(
            Standings(
                "Round 2",
                ["Buchholz", "Progressive"],
                [
                    PlayerStanding(Player("bob"), 1.5, [1.5, 2.5]),
                    PlayerStanding(Player("alice"), 1, [2.5, 1]),
                    PlayerStanding(Player("charlie"), 1, [1.5, 2]),
                    PlayerStanding(Player("dave"), 0.5, [2.5, 0.5])
                ]
            ), standings)

    def test_generate_standings_with_two_tie_breaker_where_first_decides_being_progressive(self):
        tournament = Tournament(
            players=[
                Player("alice"),
                Player("bob"),
                Player("charlie"),
                Player("dave")
            ],
            rounds=[
                RoundPairing("Round 1", [
                    Result(Player("alice"), Player("bob"), 0),
                    Result(Player("charlie"), Player("dave"), 1)
                ]),
                RoundPairing("Round 2", [
                    Result(Player("charlie"), Player("alice"), 0),
                    Result(Player("dave"), Player("bob"), 0.5)
                ])
            ]
        )
        standings = self.unit.generate(tournament, [Progressive(), Buchholz()])
        self.assertEqual(
            Standings(
                "Round 2",
                ["Progressive", "Buchholz"],
                [
                    PlayerStanding(Player("bob"), 1.5, [2.5, 1.5]),
                    PlayerStanding(Player("charlie"), 1, [2, 1.5]),
                    PlayerStanding(Player("alice"), 1, [1, 2.5]),
                    PlayerStanding(Player("dave"), 0.5, [0.5, 2.5])
                ]
            ), standings)
