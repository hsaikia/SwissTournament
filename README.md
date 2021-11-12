# SwissTournament
A Swiss Tournament Pairing Generator written for the [3rd Muenchener Kaffeehaus Chess Tournament](https://www.meetup.com/Chess-Munich/events/svkrqsyccqbdb/).

## Pre-requirements
- Install dependencies to your environment 
```
pip install -r requirements.txt
```
## How to use
- Execute the cli to display the help with the usage
```
python swiss_tournament.py
```
## Test that everything is working as expected
- Run all tests from the project
```
pytest
```
NOTE: Tests will try to generate files under directory `/tmp/`
## Help for each command
- How to generate a tournament
```
python swiss_tournament.py create-tournament --help
```
- How to generate standings from the current tournament state
```
python swiss_tournament.py generate_standings --help
```
- How to generate new round from the current tournament state
```
python swiss_tournament.py generate_new_round --help
```
- How to update the current tournament state from an existing round pairing with results
```
python swiss_tournament.py process_results --help
```

## Example of usage in a tournament
1. Create a new tournament 
```
python swiss_tournament.py create-tournament ~/3_kaffeehaus_chess_tournament/tournament
```
2. Edit your players manually with a text editor in the file (yaml format): `~/3_kaffeehaus_chess_tournament/tournament.yaml`
3. Generate the initial standings 
```
python swiss_tournament.py generate_standings ~/3_kaffeehaus_chess_tournament/tournament ~/3_kaffeehaus_chess_tournament/standings_initial
```
4. Look at your standings! (markdown format): `~/3_kaffeehaus_chess_tournament/standings_initial.md`
5. Generate the pairing for the first round
```
python swiss_tournament.py generate_new_round ~/3_kaffeehaus_chess_tournament/tournament "Round 1"  ~/3_kaffeehaus_chess_tournament/round_1
```
6. Look at your new round! (markdown format): `~/3_kaffeehaus_chess_tournament/round_1.md`
7. Update the round with the results, by modifying the result in the file (yaml format): `~/3_kaffeehaus_chess_tournament/round_1.yaml`
- Use 1 for White wins
- Use 0 for Black wins
- Use 0.5 for Tie
8. Introduce the results of the last round into your tournament
```
python swiss_tournament.py process_results ~/3_kaffeehaus_chess_tournament/tournament ~/3_kaffeehaus_chess_tournament/round_1
```
9. Generate the standings after round 1 
```
python swiss_tournament.py generate_standings ~/3_kaffeehaus_chess_tournament/tournament ~/3_kaffeehaus_chess_tournament/standings_round_1
```
10. Repeat steps from 5 to 10 for each new round, changing the files for the rounds accordingly. 
When there is no possibility to generate a new round because of repeating pairings, the system will
generate an empty pairing
  
## TODOs and Future Improvements
- Improve pairing method by using [Dutch pairing system](https://en.wikipedia.org/wiki/Swiss-system_tournament#Dutch_system)
- Create a tournament config file to avoid typing the tournament file every command
- Add tournament name to tournament file
- Create a markdown exporter for the tournament to have a final global report
- Create cleaner and safer tests by not writing to `/tmp/`
