from .event import Event
from ..errors.game_action_error import GameActionError

class SpellManagementEvent(Event):

    def __init__(self, entity, enemy):
        super().__init__(entity)
        self.enemy = enemy
        self.stage = 0
        self.selected_index = None

    def get_options(self):
        """Return options based on current stage."""
        if self.stage == 0:
            options = []
            for spell in self.entity.known_spells:
                options.append(spell.name)
            options.append("back")
            return options
        elif self.stage == 1:
            return ["yes", "no"]
        else:
            raise GameActionError("Invalid stage")
        
    def resolve(self, dungeon, action):
        """Process user action based on current stage."""
        if action == "back":
            # Pop this event and return to previous
            dungeon.pop_event()
            return
        if self.stage == 0:
            self._handle_item_selection(dungeon, action)
        elif self.stage == 1:
            self._handle_confirmation(dungeon, action)

    def _handle_item_selection(self, dungeon, action):
        """Handle selection from the item list (stage 0)."""
        # Try to find the item by name first (in case the UI sends item names directly)
        for i, spell in enumerate(self.entity.known_spells):
            if spell.name.lower() == action.lower():
                self.selected_index = i
                dungeon._msg(spell.description)
                self.stage = 1
                return
        # Otherwise try to parse as index
        index = self._parse_index_from_action(action, len(self.entity.known_spells))
        if index is None:
            raise GameActionError("Invalid selection")
        self.selected_index = index
        dungeon._msg(self.entity.known_spells[index].description)
        self.stage = 1

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
            self._perform_use(dungeon)
        elif action_str == "no":
            # Go back to action options
            self.stage = 1
        else:
            raise GameActionError(f"Invalid response: {action}")

    def _perform_use(self, dungeon):
        """Use the selected item and clean up."""
        spell = self.entity.known_spells[self.selected_index]
        dungeon._msg(spell.cast_spell(dungeon.player, self.enemy))
        dungeon._msg(f"{spell.name} used.")
        dungeon.pop_event()

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

