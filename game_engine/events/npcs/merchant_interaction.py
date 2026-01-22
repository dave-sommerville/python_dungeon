from ..event import Event
from ...game_states import GameState
from ...errors.game_action_error import GameActionError
from .merchant_item import MerchantItemEvent
class MerchantEvent(Event):
  def __init__(self, entity):
    super().__init__(entity)

  def get_options(self):
    return self.entity.print_character_inventory()
  def resolve(self, dungeon, action):
        print(action)
        if action == "back":
            dungeon.pop_event()
            dungeon.state = GameState.MAIN_MENU
            return
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(self.entity.inventory):
                item = self.entity.inventory[index]
                dungeon._msg(f"It is a {item.item_description()} for {item.cost} gold pieces")
                dungeon.push_event(MerchantItemEvent(item, index, self))
                dungeon.state = GameState.MAIN_MENU
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
            if index_part.isdigit():
                index = int(index_part)
                if 0 <= index < len(self.entity.inventory):
                    item = self.entity.inventory[index]
                    dungeon._msg(f"It is a {item.item_description()} for {item.cost} gold pieces")
                    dungeon.push_event(MerchantItemEvent(item, index, self))
                    return
        raise GameActionError("Invalid input")

