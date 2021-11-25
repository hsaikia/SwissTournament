from typing import List, Optional

from swiss_tournament.data.player import Player
from swiss_tournament.data.round_pairing import RoundPairing
from swiss_tournament.data.tournament import Tournament
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


DEFAULT_TIE_BREAKERS = []
tournament_parser: TournamentParser = YamlTournamentParser()
round_parser: RoundParser = YamlRoundParser()

round_exporters: List[RoundExporter] = [YamlRoundExporter(), MarkdownRoundExporter()]
tournament_exporters: List[TournamentExporter] = [YamlTournamentExporter()]
standings_exporters: List[StandingsExporter] = [MarkdownStandingsExporter()]

standings_generator: StandingsGenerator = StandingsGenerator()
tournament_updater: TournamentUpdater = TournamentUpdater()
round_generator: RoundGenerator = RoundGenerator()


class Commands:

    def generate_new_round(self, tournament_file: str, name: str, output_file: str):
        """

        :param tournament_file: Tournament to generate the new round from (without extension). Example: my_tournament
        :param name: Name of the new round. Example: "Round 1"
        :param output_file: Output file to write to (without extension). Example: round_1
        """
        tournament = tournament_parser.parse(tournament_file)
        new_round_pairing = round_generator.generate(tournament)
        new_round = RoundPairing(name, new_round_pairing)
        for exporter in round_exporters:
            exporter.export(new_round, output_file)

    def process_results(self, tournament_file: str, round_file: str, new_tournament_file: Optional[str] = None):
        """

        :param tournament_file: Tournament file to update (without extension). Example: my_tournament_after_round_1
        :param round_file: Round file with results to add to the tournament (without extension). Example: round_2
        :param new_tournament_file: New tournament file output (without extension): Example: my_tournament_after_round_2
        """
        tournament = tournament_parser.parse(tournament_file)
        round_results = round_parser.parse(round_file)
        tournament_updater.update(tournament, round_results)
        for exporter in tournament_exporters:
            exporter.export(tournament, new_tournament_file or tournament_file)

    def generate_standings(self, tournament_file: str, output_file: str, tie_breakers: List[str] = None):
        """

        :param tournament_file: Tournament file to update (without extension). Example: my_tournament_after_round_1
        :param output_file: Output file for standings (without extension). Example: standings_after_round_1
        :param tie_breakers: Tie breakers to use in order. Example [Buchholz, Cumulative, BuchholzMinus1, BuchholzMinus2, MedianBuchholz]
        """
        if tie_breakers is None:
            tie_breakers = DEFAULT_TIE_BREAKERS
        tournament = tournament_parser.parse(tournament_file)
        tie_breakers_instances = list(
            map(lambda name: _get_class("swiss_tournament.step.tie_breaker." + name)(), tie_breakers)
        )
        standings = standings_generator.generate(tournament, tie_breakers_instances)
        for exporter in standings_exporters:
            exporter.export(standings, output_file)

    def create_tournament(self, output_file: str):
        """

        :param output_file: Tournament file to create (without extension). Example: my_tournament
        """
        tournament = Tournament([Player("Alice"), Player("Bob")], [])
        for exporter in tournament_exporters:
            exporter.export(tournament, output_file)
