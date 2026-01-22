from ..event import Event
from ..inventory.inventory_management import InventoryManagementEvent
from ...errors.game_action_error import GameActionError
from ...game_states import GameState

class CombatInventoryEvent(Event):
    """Event for managing inventory during combat. Only allows 'use' action."""
    
    def __init__(self, entity, player):
        super().__init__(entity)
        self.player = player

    def get_options(self):
        return self.player.print_character_inventory()
    
    def resolve(self, dungeon, action):
        if action == "back":
            # Pop this event and return to combat
            dungeon.pop_event()
            dungeon.state = GameState.MAIN_MENU
            return
        
        index = self._parse_index_from_action(action, len(self.player.inventory))
        if index is None:
            raise GameActionError("Invalid selection")
        
        item = self.player.inventory[index]
        dungeon._msg(item.item_description())
        
        # Push unified inventory management event with 'use' mode only
        inventory_event = InventoryManagementEvent(
            entity=self.player,
            mode="use",
            items_list=self.player.inventory,
            is_combat=True
        )
        # Pre-select the item for immediate use confirmation
        inventory_event.selected_index = index
        inventory_event.stage = 1  # Skip to action selection stage
        dungeon.push_event(inventory_event)

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


