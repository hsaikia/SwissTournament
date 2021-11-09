from abc import ABC


class TournamentParser(ABC):
    def parse(self, file_name: str):
        pass


class YamlTournamentParser(TournamentParser):
    def parse(self, file_name: str):
        pass
