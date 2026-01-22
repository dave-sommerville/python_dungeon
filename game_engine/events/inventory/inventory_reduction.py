from ..event import Event
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
from .inventory_management import InventoryManagementEvent

class InventoryReductionEvent(Event):
    """Event for reducing inventory when it's overloaded.
    
    Used when the player finds items but their inventory is full.
    Forces the player to discard items until there's room.
    """

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
            dungeon.pop_event()
            if dungeon.current_event is None:
                dungeon.state = GameState.MAIN_MENU
            return
            
        if self.confirmed:
            action_str = str(action).lower().strip()
            
            # Handle indexed format like "0: yes" or "1: no"
            if ":" in action_str:
                action_str = action_str.split(":", 1)[1].strip()
            
            # Handle pure numeric indices (0 = yes, 1 = no)
            if action_str == "0":
                action_str = "yes"
            elif action_str == "1":
                action_str = "no"
            
            if action_str == "yes":
                self._discard_item(dungeon)
                return
            elif action_str == "no":
                self.confirmed = False
                return
                
        # Not confirmed yet - parse selection
        # Try to find the item by name first (in case the UI sends item names directly)
        for i, item in enumerate(self.entity.loot_items):
            if item.name.lower() == action.lower():
                self.select_item_to_discard(dungeon, i)
                return
        
        # Otherwise try to parse as index
        index = self._parse_index_from_action(action, len(self.entity.loot_items))
        if index is not None:
            self.select_item_to_discard(dungeon, index)
            return
        
        raise GameActionError("Invalid selection")

    def select_item_to_discard(self, dungeon, index):
        """Select an item to discard and ask for confirmation."""
        dungeon._msg(f"Are you sure you want to discard {self.entity.loot_items[index].name}?")
        self.item_index = index
        self.confirmed = True

    def _discard_item(self, dungeon):
        """Discard the selected item and check if inventory is now manageable."""
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
            dungeon._msg(f"Items added to inventory")
            
            # Pop this event and return to main menu
            dungeon.pop_event()
            if dungeon.current_event is None:
                dungeon.state = GameState.MAIN_MENU
        else:
            # Continue selection process - show how many more items to discard
            remaining_to_discard = len(remaining_found) - dungeon.player.get_inventory_room()
            dungeon._msg(f"You need to discard {remaining_to_discard} more item(s)")
            self.confirmed = False

    def _parse_index_from_action(self, action, max_index):
        """Parse an index from action string. Handles both plain digits and "0: Item Name" format."""
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < max_index:
                return index
        elif isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                if 0 <= index < max_index:
                    return index
        return None
