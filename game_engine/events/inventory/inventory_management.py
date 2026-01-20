from ..event import Event
from ...game_states import GameState
from ...errors.game_action_error import GameActionError
from ...events.inventory.inventory_item import InventoryItemEvent
class InventoryManagementEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)

    def get_options(self):
        return self.entity.print_character_inventory()

    def resolve(self, dungeon, action):
        player = dungeon.player
        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            return
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(player.inventory):
                item = player.inventory[index]
                dungeon._msg(item.item_description())
                dungeon.current_event = InventoryItemEvent(item, index)
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                if 0 <= index < len(player.inventory):
                    item = player.inventory[index]
                    dungeon._msg(item.item_description())
                    dungeon.current_event = InventoryItemEvent(item, index)
                    return
        raise GameActionError("Invalid input")