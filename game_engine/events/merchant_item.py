from .event import Event
from ..game_action_error import GameActionError
from ..game_states import GameState
class MerchantItemEvent(Event):
  def __init__(self, entity, index, prev_event):
    super().__init__(entity)
    self.index = index
    self.prev_event = prev_event

  def get_options(self):
    return ["buy","back"]
  
  def resolve(self, dungeon, action):
    match action:
      case "buy":
        dungeon.player.add_to_inventory(self.entity)
        dungeon.message_buffer.append("Item purchased")
        del self.prev_event.entity.inventory[self.index]
        dungeon.current_event = self.prev_event
        dungeon.state = GameState.MAIN_MENU
      case "back":
        dungeon.current_event = self.prev_event
        dungeon.state = GameState.MAIN_MENU
      case _:
        raise GameActionError("Invalid Action")
