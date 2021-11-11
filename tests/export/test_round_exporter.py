import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.export.round_exporter import YamlRoundExporter, MarkdownRoundExporter
from swiss_tournament.parse.round_parser import YamlRoundParser


class YamlRoundExporterTestCase(unittest.TestCase):
    unit = YamlRoundExporter()
    parser = YamlRoundParser()

    def test_export_empty_pairing(self):
        file_name = "/tmp/emptyPairing"
        pairing = RoundPairing("Round 1", [])
        self.unit.export(pairing, file_name)
        self.assertEqual(pairing, self.parser.parse(file_name))

    def test_export_pairing_with_matches(self):
        file_name = "/tmp/pairingWithMatches"
        pairing = RoundPairing("Round 1", [
            Result(Player("alice"), Player("bob"), None),
            Result(Player("charlie"), Player("dave"), 0.5)
        ])
        self.unit.export(pairing, file_name)
        self.assertEqual(pairing, self.parser.parse(file_name))


class MarkdownRoundExporterTestCase(unittest.TestCase):
    unit = MarkdownRoundExporter()

    def test_export_empty_pairing(self):
        file_name = "/tmp/emptyPairing"
        pairing = RoundPairing("Round 1", [])
        self.unit.export(pairing, file_name)

    def test_export_pairing_with_matches(self):
        file_name = "/tmp/pairingWithMatches"
        pairing = RoundPairing("Round 1", [
            Result(Player("alice"), Player("bob"), None),
            Result(Player("charlie"), Player("dave"), 0.5)
        ])
        self.unit.export(pairing, file_name)
