import pathlib
import unittest

from swiss_tournament.data.player import Player
from swiss_tournament.data.result import Result
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.parse.round_parser import YamlRoundParser


class YamlRoundParserTestCase(unittest.TestCase):
    unit = YamlRoundParser()
    test_path = str(pathlib.Path(__file__).parent.parent.resolve())

    def test_load_empty_round(self):
        file_path = '/'.join((self.test_path, 'test_files', 'emptyPairing'))
        pairing = self.unit.parse(file_path)
        self.assertEqual(RoundPairing("Round 1", []), pairing)

    def test_load_round_with_rounds(self):
        file_path = '/'.join((self.test_path, 'test_files', 'pairingWithMatches'))
        pairing = self.unit.parse(file_path)
        self.assertEqual(
            RoundPairing("Round 1", [
                Result(Player("alice"), Player("bob"), None),
                Result(Player("charlie"), Player("dave"), 0.5)
            ]), pairing)
