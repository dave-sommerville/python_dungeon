from ..event import Event
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
from .inventory_management import InventoryManagementEvent

class InventoryReductionEvent(Event):

    def __init__(self, entity, player=None, found_items=None):
        super().__init__(entity)
        self.player = player
        self.found_items = found_items or []  # Track which items are newly found
        self.confirmed = False
        self.item_index = None
        
    def get_options(self):
        if self.confirmed:
            return ["yes", "no"]
        else:
            options = []
            for item in self.entity.loot_items:
                options.append(item.name)
            options.append("back")
            return options
            
    def resolve(self, dungeon, action):
        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            dungeon.current_event = None
            return
            
        if self.confirmed:
            if action == "yes":
                discarded_item = self.entity.loot_items.pop(self.item_index)
                
                # If the discarded item was in player inventory, remove it
                if discarded_item in dungeon.player.inventory:
                    dungeon.player.inventory.remove(discarded_item)
                
                # Check if remaining found items now fit in inventory
                remaining_found = [item for item in self.entity.loot_items if item in self.found_items]
                if len(remaining_found) <= dungeon.player.get_inventory_room():
                    # Add all remaining found items to inventory
                    for item in remaining_found:
                        dungeon.player.add_to_inventory(item)
                    # Clear the chamber items since we've successfully picked them up
                    dungeon.player.current_chamber.chamber_items = []
                    dungeon.state = GameState.INVENTORY_MANAGEMENT
                    dungeon.current_event = InventoryManagementEvent(dungeon.player)
                    dungeon._msg(f"Items added to inventory")
                else:
                    # Continue selection process - show how many more items to discard
                    remaining_to_discard = len(remaining_found) - dungeon.player.get_inventory_room()
                    dungeon._msg(f"You need to discard {remaining_to_discard} more item(s)")
                    self.confirmed = False
                return
            elif action == "no":
                self.confirmed = False
                return
                
        # Not confirmed yet - parse selection
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(self.entity.loot_items):
                self.select_item_to_discard(dungeon, index)
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                if 0 <= index < len(self.entity.loot_items):
                    self.select_item_to_discard(dungeon, index)
                    return
        raise GameActionError("Invalid input")
        
    def select_item_to_discard(self, dungeon, index):
        dungeon._msg(f"Are you sure you want to discard {self.entity.loot_items[index].name}?")
        self.item_index = index
        self.confirmed = True
