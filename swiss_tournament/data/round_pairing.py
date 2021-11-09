from typing import List

from swiss_tournament.data.player import Player


class RoundPairing:
    pairing: List[(Player, Player, int)]
