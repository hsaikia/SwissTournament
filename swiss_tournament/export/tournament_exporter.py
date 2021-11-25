from abc import ABC

import yaml

from swiss_tournament.data.tournament import Tournament
from swiss_tournament.export.data_class_to_dict import TournamentToDict


class TournamentExporter(ABC):
    def export(self, tournament: Tournament, file_name: str):
        pass


class YamlTournamentExporter(TournamentExporter):
    def export(self, tournament: Tournament, file_name: str):
        document = TournamentToDict.parse(tournament)

        with open(f'{file_name}.yaml', 'w') as outfile:
            yaml.dump(document, outfile, default_flow_style=False, sort_keys=False)
