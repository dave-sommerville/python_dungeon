from ..event import Event
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
class InventoryManagementEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
        self.item_counter = 0
    def get_options(self):
        option = []
        for item in self.entity.loot_items:
            option.append(item.name)
        return option
    def resolve(self, dungeon, action):
        self.item_counter = len(self.entity.loot_items) - dungeon.player.get_inventory_room()
        if len(self.item_counter) <= 0:
            dungeon.current_event = None
            dungeon.state = GameState.MAIN_MENU
            return
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