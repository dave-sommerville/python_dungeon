from enum import Enum, auto

class GameState(Enum):
    INITIALIZING = auto()
    MAIN_MENU = auto()
    INVENTORY_MANAGEMENT = auto()
    SPELL_MANAGEMENT = auto()
    COMBAT = auto()
    NPC_INTERACTION = auto()
    MERCHANT = auto()
    SKILL_CHECK = auto()
    LEVELLING_UP = auto()
    GAME_OVER = auto()
