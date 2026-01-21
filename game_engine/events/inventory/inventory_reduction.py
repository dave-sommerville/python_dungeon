from ..event import Event
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
class InventoryReductionEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
        self.confirmed = False
        self.item_index = None
    def get_options(self):
        if self.confirmed:
            return ["confirm", "back"]
        else:
            options = []
            for item in self.entity.loot_items:
                options.append(item.name)
            return options
    def resolve(self, dungeon, action):
        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            return
        if not self.confirmed:
            if action == "confirm":
                self.confirmed = True
                del self.entity.loot_items[self.item_index]
                return
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(self.entity.loot_items):
                self.is_complete(dungeon, index)
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                self.is_complete(dungeon, index)
                return
        raise GameActionError("Invalid input")
    def is_complete(self, dungeon, index):
        dungeon._msg(f"Are you sure you want to discard {self.entity.loot_items[index].name}?")
        self.item_index = index
        self.confirmed = False
        if len(self.entity.loot_items) == dungeon.player.max_inventory_size:
            dungeon.player.inventory = self.entity.loot_items.copy()
            dungeon.state = GameState.MAIN_MENU
            dungeon.current_event = None
