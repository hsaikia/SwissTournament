from abc import ABC

from swiss_tournament.data.round_pairing import RoundPairing


class RoundExporter(ABC):
    def export(self, round_pairing: RoundPairing, output_file: str):
        pass


class MarkdownRoundExporter(RoundExporter):
    def export(self, round_pairing: RoundPairing, output_file: str):
        pass


class YamlRoundExporter(RoundExporter):
    def export(self, round_pairing: RoundPairing, output_file: str):
        pass
