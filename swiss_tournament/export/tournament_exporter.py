from abc import ABC

from swiss_tournament.data.tournament import Tournament


class TournamentExporter(ABC):
    def export(self, tournament: Tournament, file_name: str):
        pass


class YamlTournamentExporter(TournamentExporter):
    def export(self, tournament: Tournament, file_name: str):
        pass
