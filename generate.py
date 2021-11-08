#import math

import networkx as nx
from functools import cmp_to_key

NEG_INF = -100000000
DUMMY = "DUMMY_PLAYER"
MAX_ROUNDS = 6

class Player():
	name : str
	won : int
	lost : int
	drawn : int
	whites : int
	blacks: int
	score : float

	def __init__(self, _name):
		self.name = _name
		self.won = 0
		self.lost = 0
		self.drawn = 0
		self.whites = 0
		self.blacks = 0
		self.score = 0.0

class Pairing():
	i1: int
	i2: int
	s1: float
	s2: float

def report_game(w: Player, b: Player, res: str):
	if res == "NP":
		return
	w.whites = w.whites + 1
	b.blacks = b.blacks + 1
	if res == "W":
		w.won += 1
		w.score += 1.0
		b.lost += 1
	elif res == "B":
		b.won += 1
		b.score += 1.0
		w.lost += 1
	elif res == "D":
		w.drawn += 1
		b.drawn += 1
		w.score += 0.5
		b.score += 0.5

def pairing_cost(player1 : Player, player2 : Player):
	score_diff = abs(player1.score - player2.score)
	color_diff = abs(player1.whites - player2.blacks) + abs(player1.blacks - player2.whites)
	#print(f"P1 {player1.name} P2 {player2.name} Score Diff {score_diff} Color Diff {color_diff}")
	return -(1000 * score_diff + color_diff)

def read_input(input_file: str):
	file = open(input_file, "r")
	inp = [line.strip() for line in file.readlines() if line.strip()]
	return inp

def calculate_standings(input_str : [str]):
	read_players = False
	read_results = -1
	players = []
	results = []
	results_curr = []
	player_map = dict()
	
	for x in input_str:
		if x == "P":
			read_players = True
			continue
		if x == "R":
			read_players = False
			read_results = read_results + 1
			continue
		if read_players:
			player_map[x] = len(players)
			players.append(Player(x))
			continue
		if read_results == len(results):
			results_curr.append(x)
		if read_results > len(results):
			results.append(results_curr)
			results_curr = []
			results_curr.append(x)

	if len(results_curr) > 0:
		results.append(results_curr)

	# If odd number of players, add a dummy
	if len(players) % 2 != 0:
		player_map[DUMMY] = len(players)
		players.append(Player(DUMMY))

	# Populate Graph
	G = nx.Graph()
	n = len(players)
	for i in range(n):
		G.add_node(i)

	for i in range(n):
		for j in range(i + 1, n):
			G.add_edge(i, j, weight=0.0)

	# calculate wins and losses from results
	for rnd in results:
		for game in rnd:
			arr = game.split(":")
			id1 = player_map[arr[0]]
			id2 = player_map[arr[1]]
			if arr[0] != DUMMY and arr[1] != DUMMY:	
				report_game(players[id1], players[id2], arr[2])

			G[id1][id2]['weight'] = NEG_INF
			if arr[0] == DUMMY or arr[1] == DUMMY:
				G[id1][id2]['weight'] = 2 * NEG_INF

	return players, results, G

def compare_pairing(pa : Pairing, pb : Pairing):
	if pa.s1 + pa.s2 < pb.s1 + pb.s2:
		return 1
	elif pa.s1 + pa.s2 > pb.s1 + pb.s2:
		return -1
	elif max(pa.s1, pa.s2) < max(pb.s1, pb.s2):
		return 1
	elif max(pa.s1, pa.s2) > max(pb.s1, pb.s2):
		return -1
	return 0	

def create_pairings(players, G):
	n = len(players)
	for i in range(n):
		for j in range(i + 1, n):
			if G[i][j]['weight'] > NEG_INF :
				G[i][j]['weight'] = pairing_cost(players[i], players[j])
	pairing_set = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)
	pairings = []
	for p in pairing_set:
		pr = Pairing()
		pr.i1, pr.i2 = p
		pr.s1 = players[pr.i1].score
		pr.s2 = players[pr.i2].score
		pairings.append(pr)
	return sorted(pairings, key=cmp_to_key(compare_pairing))

def write_pairings(pairings, players, txt_file: str, md_file: str, rnd : int):
	file = open(txt_file, "a")
	file_md = open(md_file, "a")
	file.write("\nR")
	file_md.write(f"\n## Round {rnd} pairings\n")
	file_md.write("|Board|:white_circle:|:black_circle:|\n")
	file_md.write("|---|---|---|\n")
	board_number = 1
	for p in pairings:
		x, y = p.i1, p.i2
		more_whites_x = players[x].whites - players[x].blacks
		more_whites_y = players[y].whites - players[y].blacks
		if more_whites_x < more_whites_y :
			file.write(f"\n{players[x].name}:{players[y].name}:NP")
			file_md.write(f"|{board_number}|{players[x].name}|{players[y].name}|\n")
		else:
			file.write(f"\n{players[y].name}:{players[x].name}:NP")
			file_md.write(f"|{board_number}|{players[y].name}|{players[x].name}|\n")
		board_number += 1
	file.close()
	file_md.close()

def write_pretty(output_file: str, ranked : [Player], tournament_title: str):
	file = open(output_file, "w")
	file.write(f"# {tournament_title}\n")
	file.write("## Standings\n")
	file.write("|Rank|Name|W-D-L|Score|Colors|\n")
	file.write("|---|---|---|---|---|\n")
	rank = 0
	pl_count = 0
	old_score = 10000
	for pl in ranked:
		if pl.name == DUMMY:
			continue
		pl_count += 1
		if pl.score < old_score:
			rank = pl_count
		played = pl.won + pl.drawn + pl.lost
		file.write(f"|{rank}|{pl.name.ljust(15)}|{pl.won}-{pl.drawn}-{pl.lost}|{pl.score}/{played}|:white_circle: {pl.whites} :black_circle: {pl.blacks}|\n")
		old_score = pl.score
		
	file.close()

def write_previous_results(md_file: str, results: [str], players : [Player]):
	file = open(md_file, "a")
	for rnd_idx in range(len(results)):
		file.write(f"\n## Round {rnd_idx + 1} results\n")
		for game in results[rnd_idx]:
			arr = game.split(":")
			if arr[2] == "W":
				file.write(f"- **{arr[0]}** :white_circle: *beat* {arr[1]} :black_circle:\n")
			elif arr[2] == "B":
				file.write(f"- {arr[0]} :white_circle: *lost to* **{arr[1]}** :black_circle:\n")
			elif arr[2] == "D":
				file.write(f"- {arr[0]} :white_circle: *drew with* {arr[1]} :black_circle:\n")
	file.close()

def main():
	tournament_title = "2. MÃ¼nchner Kaffeehaus Open"
	# Text file where results are updated by hand
	txt_file = "input.txt"
	# Markdown file where results are published in a presantable format
	md_file = "tournament.md"
	status = read_input(txt_file)
	players, results, G = calculate_standings(status)
	ranked = sorted(players, key=lambda x : x.score, reverse=True)
	write_pretty(md_file, ranked, tournament_title)

	rounds = len(results)
	if rounds < MAX_ROUNDS :
		pairings = create_pairings(players, G)
		write_pairings(pairings, players, txt_file, md_file, rounds + 1)
	write_previous_results(md_file, results, players)

if __name__ == "__main__":
    main()