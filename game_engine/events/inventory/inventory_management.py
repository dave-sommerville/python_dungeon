from ..event import Event
from ...game_states import GameState
from ...errors.game_action_error import GameActionError
from ...events.inventory.inventory_item import InventoryItemEvent
class InventoryManagementEvent(Event):

    def __init__(self, entity, type_of_management, items_list):
        super().__init__(entity)
        self.stage = 0
        self.type_of_management = type_of_management
        self.index = None
        self.items_list = items_list

    def get_options(self):
        if self.stage is 0:
            options = self.print_list()
        elif self.stage is 1:
            options = self.print_options()
        elif self.stage is 2:
            options = ["yes", "no"]
        else: 
            raise GameActionError
        return options
    
    def resolve(self, dungeon, action):
        player = dungeon.player
        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            dungeon.current_event = None
            return
        if self.stage is 0:
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
            if isinstance(action, str) and action.isdigit():
                index = int(action)
                if 0 <= index < len(self.items_list):
                        self.index = index
                        dungeon._msg(player.inventory[index].item_description())
                        self.stage = 1
                        return
            # Backwards-compatible: parse "0: Name" style
            if isinstance(action, str) and ":" in action:
                index_part = action.split(":")[0].strip()
                if index_part.isdigit():
                    index = int(index_part)
                    if 0 <= index < len(self.items_list):
                        self.index = index
                        dungeon._msg(f"You have selected {player.inventory[index].name}")
                        dungeon._msg(f"Choose your action")
                        self.stage = 1
                        return
            raise GameActionError("Invalid input")
        elif self.stage is 1:
            pass
        elif self.stage is 2:
            pass
    def print_list(self):
        options = []
        for item in self.item_list:
            options.append(item.name)
        if self.stage is not 2:
            options.append("back")
        return options
    
    def print_options(self):
        options = []
        if self.type == "use":
            options.append("use")
        if self.type == "discard":
            options.append("discard")
        if self.type == "both":
            options.append("use")
            options.append("discard")
        options.append("back")
        return options
    def use_item(self, dungeon):
        self.items_list[self.index].use_item(self.entity)
        del dungeon.player.inventory[self.index]
        dungeon.message_buffer.append("Item used.")
        dungeon.current_event = None
        dungeon.state = GameState.MAIN_MENU