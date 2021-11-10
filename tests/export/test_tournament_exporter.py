import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
from swiss_tournament.export.tournament_exporter import YamlTournamentExporter
from swiss_tournament.parse.tournament_parser import YamlTournamentParser


class YamlTournamentExporterTestCase(unittest.TestCase):
    unit = YamlTournamentExporter()
    parser = YamlTournamentParser()

    def test_export_empty_tournament(self):
        file_name = "/tmp/emptyTournament"
        tournament = Tournament(players=[], rounds=[])
        self.unit.export(tournament, file_name)
        self.assertEqual(tournament, self.parser.parse(file_name))

    def test_export_tournaments_without_rounds(self):
        file_name = "/tmp/tournamentWithoutRounds"
        tournament = Tournament(players=[Player('Alice'), Player('Bob')], rounds=[])
        self.unit.export(tournament, file_name)
        self.assertEqual(tournament, self.parser.parse(file_name))

    def test_export_tournaments_with_rounds(self):
        file_name = "/tmp/tournamentWithRounds"
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
        self.unit.export(tournament, file_name)
        self.assertEqual(tournament, self.parser.parse(file_name))
