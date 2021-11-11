import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.player_standing import PlayerStanding
from swiss_tournament.data.standings import Standings
from swiss_tournament.export.standings_exporter import MarkdownStandingsExporter


class MarkdownStandingsExporterTestCase(unittest.TestCase):
    unit = MarkdownStandingsExporter()

    def test_export_empty_standings(self):
        file_name = "/tmp/emptyStandings"
        standings = Standings("Round 1", [], [])
        self.unit.export(standings, file_name)

    def test_export_standings_without_tie_breakers(self):
        file_name = "/tmp/StandingsWithoutTieBreakers"
        standings = Standings(round="Round 1", tie_breakers=[], standings=[
            PlayerStanding(Player("Alice"), 2, []),
            PlayerStanding(Player("Bob"), 1, []),
            PlayerStanding(Player("Charlie"), 1, [])
        ])
        self.unit.export(standings, file_name)

    def test_export_standings_with_tie_breakers(self):
        file_name = "/tmp/StandingsWithTieBreakers"
        standings = Standings(round="Round 1", tie_breakers=[
            "Buchholz",
            "Progressive"
        ], standings=[
            PlayerStanding(Player("Alice"), 2, [2, 3]),
            PlayerStanding(Player("Bob"), 1, [3, 2]),
            PlayerStanding(Player("Charlie"), 1, [3, 2])
        ])
        self.unit.export(standings, file_name)
