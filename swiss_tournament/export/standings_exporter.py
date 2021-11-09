from abc import ABC

from swiss_tournament.data.standings import Standings


class StandingsExporter(ABC):
    def export(self, standings: Standings, file_name: str):
        pass


class MarkdownStandingsExporter(ABC):
    def export(self, standings: Standings, file_name: str):
        pass
