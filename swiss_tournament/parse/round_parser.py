from abc import ABC

from swiss_tournament.data.round_pairing import RoundPairing


class RoundParser(ABC):
    def parse(self, file_name: str) -> RoundPairing:
        pass


class YamlRoundParser(ABC):
    def parse(self, file_name: str) -> RoundPairing:
        pass
