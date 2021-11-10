from abc import ABC

import yaml

from swiss_tournament.data.tournament import Tournament
from swiss_tournament.parse.dict_to_data_class import DictToTournament


class TournamentParser(ABC):
    def parse(self, file_name: str) -> Tournament:
        pass


class YamlTournamentParser(TournamentParser):
    def parse(self, file_name: str) -> Tournament:
        with open(f"{file_name}.yaml", "r") as stream:
            document = yaml.load(stream, Loader=yaml.Loader)
            tournament = DictToTournament.parse(document)
            return tournament
