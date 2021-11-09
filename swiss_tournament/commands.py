from typing import List, Optional

from swiss_tournament.parse.round_parser import RoundParser, YamlRoundParser
from swiss_tournament.export.standings_exporter import MarkdownStandingsExporter, StandingsExporter
from swiss_tournament.step.standings_generator import StandingsGenerator
from swiss_tournament.export.tournament_exporter import TournamentExporter, YamlTournamentExporter
from swiss_tournament.parse.tournament_parser import YamlTournamentParser, TournamentParser
from swiss_tournament.export.round_exporter import YamlRoundExporter, RoundExporter, MarkdownRoundExporter
from swiss_tournament.step.round_generator import RoundGenerator
from swiss_tournament.step.tie_breaker import Buchholz
from swiss_tournament.step.tournament_updater import TournamentUpdater


def _get_class(kls: str):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class Commands:
    DEFAULT_TIE_BREAKERS = ["Bucholz", "MedianBucholz", "Progressive"]
    tournament_parser: TournamentParser = YamlTournamentParser()
    round_parser: RoundParser = YamlRoundParser()

    round_exporters: List[RoundExporter] = [YamlRoundExporter(), MarkdownRoundExporter()]
    tournament_exporters: List[TournamentExporter] = [YamlTournamentExporter]
    standings_exporters: List[StandingsExporter] = [MarkdownStandingsExporter]

    standings_generator: StandingsGenerator = StandingsGenerator()
    tournament_updater: TournamentUpdater = TournamentUpdater()
    round_generator: RoundGenerator = RoundGenerator()

    def generate_new_round(self, tournament_file: str, output_file: str):
        tournament = self.tournament_parser.parse(tournament_file)
        standings = self.standings_generator.generate(tournament, [Buchholz()])
        new_round = self.round_generator.generate(tournament, standings)
        for exporter in self.round_exporters:
            exporter.export(new_round, output_file)

    def process_results(self, tournament_file: str, round_file: str, new_tournament_file: Optional[str] = None):
        tournament = self.tournament_parser.parse(tournament_file)
        round_results = self.round_parser.parse(round_file)
        self.tournament_updater.update(tournament, round_results)
        for exporter in self.tournament_exporters:
            exporter.export(tournament, new_tournament_file or tournament_file)

    def generate_standings(self, tournament_file: str, output_file: str, tie_breakers: List[str] = None):
        if tie_breakers is None:
            tie_breakers = self.DEFAULT_TIE_BREAKERS
        tournament = self.tournament_parser.parse(tournament_file)
        tie_breakers_instances = list(
            map(lambda name: _get_class("swiss_tournament.step.tie_breaker." + name)(), tie_breakers)
        )
        standings = self.standings_generator.generate(tournament, tie_breakers_instances)
        for exporter in self.standings_exporters:
            exporter.export(standings, output_file)
