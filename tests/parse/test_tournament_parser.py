import pathlib
import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.parse.tournament_parser import YamlTournamentParser


class YamlTournamentParserTestCase(unittest.TestCase):
    unit = YamlTournamentParser()
    test_path = str(pathlib.Path(__file__).parent.parent.resolve())

    def test_load_empty_tournament(self):
        file_path = '/'.join((self.test_path, 'test_files', 'emptyTournament'))
        tournament = self.unit.parse(file_path)
        self.assertEqual([], tournament.players)
        self.assertEqual([], tournament.rounds)

    def test_load_tournament_without_rounds(self):
        file_path = '/'.join((self.test_path, 'test_files', 'tournamentWithoutRounds'))
        tournament = self.unit.parse(file_path)
        self.assertEqual([Player("Alice"), Player("Bob")], tournament.players)
        self.assertEqual([], tournament.rounds)

    def test_load_tournament_with_rounds(self):
        file_path = '/'.join((self.test_path, 'test_files', 'tournamentWithRounds'))
        tournament = self.unit.parse(file_path)
        self.assertEqual(Tournament(
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
            ), tournament)
