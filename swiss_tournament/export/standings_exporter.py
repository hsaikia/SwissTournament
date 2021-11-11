from abc import ABC

from swiss_tournament.data.standings import Standings


class StandingsExporter(ABC):
    def export(self, standings: Standings, file_name: str):
        pass


class MarkdownStandingsExporter(ABC):
    def export(self, standings: Standings, file_name: str):
        with open(f'{file_name}.md', 'w') as outfile:
            outfile.write(f"\n## Standings after {standings.round}\n")
            outfile.write("|Position|Player|Points|")
            for tie_breaker in standings.tie_breakers:
                outfile.write(f"{tie_breaker}|")
            outfile.write("\n")
            outfile.write("|---|---|---|")
            for tie_breaker in standings.tie_breakers:
                outfile.write("---|")
            outfile.write("\n")
            position = 1
            for player_standing in standings.standings:
                outfile.write(f"|{position}|{player_standing.player.name}|{player_standing.points}|")
                for tie_breaker in player_standing.tie_breakers:
                    outfile.write(f"{tie_breaker}|")
                outfile.write("\n")
                position += 1
