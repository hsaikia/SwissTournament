# SwissTournament
A Swiss Tournament Pairing Generator

# How to use
- Add the player names after a `P` and a newline, one per line.
- Add the Round results after a `R` and a newline, in the format `<White Player name>:<Black Player name>:<W/B/D>` one per line.
- If the Tournament does not have any recorded results, you can already generate the pairings for the next round by running
  
  ```python
  python generate.py
  ```
  Open `tournament.md` in any markdown viewer to view the standings, pairings for the next round and the results of the previous rounds.
- Input the results of the current round by changing the `NP`s to `W` for a white win, `B` for a black win and `D` for a draw. 
- Run `python generate.py` again to generate the current standings pairings for the next round. Pairings are stopped when the maximum number of rounds is reached.
  
# TODOs and Future Improvements
  - The input and output file names, tournament title and max number of rounds are global variables currently, they can be cmdline parameters instead.
  - There are currently no tie-breaks between players in the final standings, total score being the only ranking criteria. Ties-breaks between players with equal scores can be implemented by following any of the standard tie-break calculators.
