from dataclasses import dataclass


@dataclass
class Player:
    name: str

    def __hash__(self):
        return hash(self.name)


# Fictional player to pair with non-paired people in each round
BYE = Player("bye")
