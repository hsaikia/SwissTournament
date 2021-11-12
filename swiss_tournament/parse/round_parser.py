from abc import ABC

import yaml

from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.parse.dict_to_data_class import DictToRoundPairing


class RoundParser(ABC):
    def parse(self, file_name: str) -> RoundPairing:
        pass


class YamlRoundParser(RoundParser):
    def parse(self, file_name: str) -> RoundPairing:
        with open(f"{file_name}.yaml", "r") as stream:
            document = yaml.load(stream, Loader=yaml.Loader)
            pairing = DictToRoundPairing.parse(document)
            return pairing[0]
