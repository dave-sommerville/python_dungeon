from .event import Event
from ..game_states import GameState
from ..errors.game_action_error import GameActionError

class InventoryManagementEvent(Event):
    """Unified inventory management event that handles use, discard, or both actions.
    
    Args:
        entity: The character whose inventory is being managed
        mode: One of 'use', 'discard', or 'both' - determines available actions
        items_list: List of items to display 
        is_combat: Boolean flag indicating if this is being used in combat context
    
    Stages:
        0: Display item list
        1: Show action options for selected item
        2: Confirm action (for destructive actions like discard)
    """

    def __init__(self, entity, mode="both", items_list=None, is_combat=False):
        super().__init__(entity)
        self.stage = 0
        self.mode = mode  # 'use', 'discard', or 'both'
        self.items_list = items_list if items_list is not None else entity.inventory
        self.selected_index = None
        self.selected_action = None
        self.is_combat = is_combat  # Flag to indicate combat context

    def get_options(self):
        """Return options based on current stage."""
        if self.stage == 0:
            # Show inventory items
            return self._get_item_list()
        elif self.stage == 1:
            # Show available actions for selected item
            return self._get_action_options()
        elif self.stage == 2:
            # Confirm destructive action
            return ["yes", "no"]
        else:
            raise GameActionError("Invalid stage")
    def resolve(self, dungeon, action):
        """Process user action based on current stage."""
        if action == "back":
            # Pop this event and return to previous
            dungeon.pop_event()
            if dungeon.current_event is None:
                dungeon.state = GameState.MAIN_MENU
            return
        if self.stage == 0:
            self._handle_item_selection(dungeon, action)
        elif self.stage == 1:
            self._handle_action_selection(dungeon, action)
        elif self.stage == 2:
            self._handle_confirmation(dungeon, action)

    def _handle_item_selection(self, dungeon, action):
        """Handle selection from the item list (stage 0)."""
        # Try to find the item by name first (in case the UI sends item names directly)
        for i, item in enumerate(self.items_list):
            if item.name.lower() == action.lower():
                self.selected_index = i
                dungeon._msg(item.item_description())
                self.stage = 1
                return
        # Otherwise try to parse as index
        index = self._parse_index_from_action(action, len(self.items_list))
        if index is None:
            raise GameActionError("Invalid selection")
        self.selected_index = index
        item = self.items_list[index]
        dungeon._msg(item.item_description())
        self.stage = 1

    def _handle_action_selection(self, dungeon, action):
        """Handle action selection for the item (stage 1)."""
        action_lower = action.lower()
        if action_lower == "use" and self.mode in ["use", "both"]:
            self._perform_use(dungeon)
        elif action_lower == "discard" and self.mode in ["discard", "both"]:
            # Ask for confirmation before discarding
            item = self.items_list[self.selected_index]
            dungeon._msg(f"Are you sure you want to discard {item.name}?")
            self.stage = 2
        else:
            raise GameActionError("Invalid action")

    def _handle_confirmation(self, dungeon, action):
        """Handle yes/no confirmation (stage 2)."""
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
            self._perform_discard(dungeon)
        elif action_str == "no":
            # Go back to action options
            self.stage = 1
        else:
            raise GameActionError(f"Invalid response: {action}")

    def _perform_use(self, dungeon):
        """Use the selected item and clean up."""
        item = self.items_list[self.selected_index]
        item.use_item(self.entity)
        self.items_list.remove(item)
        self.entity.inventory = self.items_list
        dungeon._msg(f"{item.name} used.")
        dungeon.pop_event()
        # If in combat, handle enemy turn
        if dungeon.current_event is None:
            dungeon.state = GameState.MAIN_MENU

    def _perform_discard(self, dungeon):
        """Discard the selected item and clean up."""
        item = self.items_list[self.selected_index]
        self.items_list.remove(item)
        dungeon._msg(f"{item.name} discarded.")
        # Pop this event and return to previous context
        if self.selected_action == "discard":
            if len(self.entity.inventory_size) is len(self.items_list):
                self.entity.inventory = self.items_list
                dungeon.pop_event()
                if dungeon.current_event is None:
                    dungeon.state = GameState.MAIN_MENU
            else:
                dungeon._msg("Select another item to discard.")
        else:
            self.entity.inventory = self.items_list
            dungeon.pop_event()
            if dungeon.current_event is None:
                dungeon.state = GameState.MAIN_MENU

    def _get_item_list(self):
        """Return list of items as options."""
        options = []
        for item in self.items_list:
            options.append(item.name)
        options.append("back")
        return options

    def _get_action_options(self):
        """Return available actions based on mode."""
        options = []
        if self.mode in ["use", "both"]:
            options.append("use")
        if self.mode in ["discard", "both"]:
            options.append("discard")
        options.append("back")
        return options

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

