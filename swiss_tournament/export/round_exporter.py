from abc import ABC

import yaml

from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.export.data_class_to_dict import PairingToDict


class RoundExporter(ABC):
    def export(self, round_pairing: RoundPairing, output_file: str):
        pass


class MarkdownRoundExporter(RoundExporter):
    def export(self, round_pairing: RoundPairing, output_file: str):
        with open(f'{output_file}.md', 'w') as outfile:
            outfile.write(f"\n## {round_pairing.name} pairings\n")
            outfile.write("|Board|:white_circle:|:black_circle:|\n")
            outfile.write("|---|---|---|\n")
            board_number = 1
            for match in round_pairing.pairing:
                outfile.write(f"|{board_number}|{match.white.name}|{match.black.name}|\n")
                board_number += 1


class YamlRoundExporter(RoundExporter):
    def export(self, round_pairing: RoundPairing, output_file: str):
        document = PairingToDict.parse(round_pairing)

        with open(f'{output_file}.yaml', 'w') as outfile:
            yaml.dump(document, outfile, default_flow_style=False, sort_keys=False)
