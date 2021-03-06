from dataclasses import dataclass
from typing import List

from swiss_tournament.data.result import Result


@dataclass
class RoundPairing:
    name: str
    pairing: List[Result]
