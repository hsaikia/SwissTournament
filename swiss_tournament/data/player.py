from dataclasses import dataclass


@dataclass
class Player:
    name: str

    def __hash__(self):
        return hash(self.name)
