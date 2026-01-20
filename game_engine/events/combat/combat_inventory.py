from ..event import Event
from .combat_use_item import CombatItemEvent
from ...errors.game_action_error import GameActionError
from ...game_states import GameState

class CombatInventoryEvent(Event):
    def __init__(self, entity, prev_event, player):
        super().__init__(entity)
        self.prev_event = prev_event
        self.player = player

    def get_options(self):
        return self.player.print_character_inventory()
    
    def resolve(self, dungeon, action):
        if action == "back":
            dungeon.current_event = self.prev_event
            dungeon.state = GameState.MAIN_MENU
            return
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(self.player.inventory):
                item = self.player.inventory[index]
                dungeon._msg(item.item_description())
                dungeon.current_event = CombatItemEvent(item, index, self)
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                if 0 <= index < len(self.player.inventory):
                    item = self.player.inventory[index]
                    dungeon._msg(item.item_description())
                    dungeon.current_event = CombatItemEvent(item, index, self)
                    return
        raise GameActionError("Invalid input")

