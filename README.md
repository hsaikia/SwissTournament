# SwissTournament

A Swiss Tournament Pairing Generator written for
the [2nd Muenchener Kaffeehaus Chess Tournament](https://www.meetup.com/Chess-Munich/events/rqwkqsyccpbgb/)
and [3rd Muenchener Kaffeehaus Chess Tournament](https://www.meetup.com/Chess-Munich/events/svkrqsyccqbdb/).

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
```
NAME
    swiss_tournament.py create-tournament

SYNOPSIS
    swiss_tournament.py create-tournament OUTPUT_FILE

POSITIONAL ARGUMENTS
    OUTPUT_FILE
        Type: str
        Tournament file to create (without extension). Example: my_tournament

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS

```

- How to generate standings from the current tournament state

```
python swiss_tournament.py generate_standings --help
```
```
NAME
    swiss_tournament.py generate_standings

SYNOPSIS
    swiss_tournament.py generate_standings TOURNAMENT_FILE OUTPUT_FILE <flags>

POSITIONAL ARGUMENTS
    TOURNAMENT_FILE
        Type: str
        Tournament file to update (without extension). Example: my_tournament_after_round_1
    OUTPUT_FILE
        Type: str
        Output file for standings (without extension). Example: standings_after_round_1

FLAGS
    --tie_breakers=TIE_BREAKERS
        Type: Optional[typing.List[str]]
        Default: None

```

- How to generate new round from the current tournament state

```
python swiss_tournament.py generate_new_round --help
```
```
NAME
    swiss_tournament.py generate_new_round

SYNOPSIS
    swiss_tournament.py generate_new_round TOURNAMENT_FILE NAME OUTPUT_FILE

POSITIONAL ARGUMENTS
    TOURNAMENT_FILE
        Type: str
        Tournament to generate the new round from (without extension). Example: my_tournament
    NAME
        Type: str
        Name of the new round. Example: "Round 1"
    OUTPUT_FILE
        Type: str
        Output file to write to (without extension). Example: round_1

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

- How to update the current tournament state from an existing round pairing with results

```
python swiss_tournament.py process_results --help
```
```
NAME
    swiss_tournament.py process_results

SYNOPSIS
    swiss_tournament.py process_results TOURNAMENT_FILE ROUND_FILE <flags>

POSITIONAL ARGUMENTS
    TOURNAMENT_FILE
        Type: str
        Tournament file to update (without extension). Example: my_tournament_after_round_1
    ROUND_FILE
        Type: str
        Round file with results to add to the tournament (without extension). Example: round_2

FLAGS
    --new_tournament_file=NEW_TOURNAMENT_FILE
        Type: Optional[typing.Optional[str]]
        Default: None
        New tournament file output (without extension): Example: my_tournament_after_round_2

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```
## Example of usage in a tournament

1. Create a new tournament

```
python swiss_tournament.py create-tournament ~/3_kaffeehaus_chess_tournament/tournament
```

2. Edit your players manually with a text editor in the file (yaml
   format): `~/3_kaffeehaus_chess_tournament/tournament.yaml`
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
7. Update the round with the results, by modifying the result in the file (yaml
   format): `~/3_kaffeehaus_chess_tournament/round_1.yaml`

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

10. Repeat steps from 5 to 10 for each new round, changing the files for the rounds accordingly. When there is no
    possibility to generate a new round because of repeating pairings, the system will generate an empty pairing

## TODOs and Future Improvements

- Improve pairing method by
  using [Dutch pairing system](https://en.wikipedia.org/wiki/Swiss-system_tournament#Dutch_system)
- Create a tournament config file to avoid typing the tournament file every command
- Add tournament name to tournament file
- Create a markdown exporter for the tournament to have a final global report
- Create cleaner and safer tests by not writing to `/tmp/`
