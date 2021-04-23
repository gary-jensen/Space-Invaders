from enum import Enum, auto

class GameState(Enum):
    START = auto()
    GAME = auto()
    END = auto()
    PAUSE = auto()