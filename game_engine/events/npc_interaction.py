from .event import Event
from ..errors.game_action_error import GameActionError

class NpcInteractionEvent(Event):
    def __init__(self, entity, enemy):
        super().__init__(entity)
        self.stage =0
        self.selected_index = None
        self.items_by_name = []
        for item in self.entity.inventory:
            self.items_by_name.append(f"{item.name} - {item.cost}")
        self.items_by_name.append("back")
    def get_options(self):
        """Return options based on current stage."""
        if self.stage == 0:
            options = ["ignore"]
            options.append(self.entity.dialogue_options)
            options.append("attempt to bargain")
            return options
        if self.stage == 1:
            return self.items_by_name
        if self.stage == 2:
            return ["yes", "no"]
    def resolve(self, dungeon, action):
        """Process user action based on current stage."""
        if self.stage == 0:
            if action == "ignore":
                # Pop this event and return to previous
                dungeon._msg("You leave the character alone")
                dungeon.pop_event()
                return
            if action == self.entity.dialogue_options[0]:
                dungeon._msg(f"{self.entity.name} replies:")
                dungeon._msg(self.entity.response_one)
            elif action == self.entity.dialogue_options[1]:
                dungeon._msg(f"{self.entity.name} replies:")
                dungeon._msg(self.entity.response_two)
            elif action == "attempt to bargain":
                dungeon._msg("You attempt to bargain with the character")
                if len(self.entity.inventory) <= 0:
                    dungeon._msg(f"But {self.entity.name} has nothing to offer")
                else:
                    dungeon._msg("Select an item you would like to buy")
                    self.stage = 1
            else:
                raise GameActionError("Invalid Action")
        elif self.stage == 1:
            if action == "back":
                dungeon._msg("You change your mind")
                self.stage = 0
            else:
                self._handle_item_selection()
        elif self.stage == 2:
            if action == "yes":
                self._handle_purchase(dungeon)
            else:
                dungeon._msg("You change your mind")
                self.stage = 1
        else:
            self.stage = 0
    def _handle_item_selection(self, dungeon, action):
        # Action is now the item name string sent by JS
        for i, item in enumerate(self.items_by_name):
            if item.name.lower() == action.lower():
                self.selected_index = i
                dungeon._msg("Would you like to purchase:")
                dungeon._msg(self.entity.inventory[i].item_description())
                self.stage = 2
                return
        raise GameActionError("Item not found.")
    def _handle_purchase(self, dungeon):
        item = self.entity.inventory[self.selected_index]
        dungeon.player.gold -= item.cost
        dungeon.player.add_to_inventory(item)
        self.entity.inventory.remove(item)