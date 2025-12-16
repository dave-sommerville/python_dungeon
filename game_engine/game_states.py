from enum import Enum, auto

class GameState(Enum):
    INITIALIZING = auto()
    MAIN_MENU = auto()
    INVENTORY_MANAGEMENT = auto()
    SPELL_MANAGEMENT = auto()
    GAME_OVER = auto()
