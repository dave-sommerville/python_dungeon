from ..event import Event
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
class MerchantItemEvent(Event):
  def __init__(self, entity, index, prev_event):
    super().__init__(entity)
    self.index = index
    self.prev_event = prev_event

  def get_options(self):
    return ["buy","back"]
  
  def resolve(self, dungeon, action):
    print(action)
    match action:
      case "buy":
        dungeon.player.add_to_inventory(self.entity)
        dungeon.message_buffer.append("Item purchased")
        del self.prev_event.entity.inventory[self.index]
        dungeon.pop_event()
        dungeon.state = GameState.INVENTORY_MANAGEMENT
      case "back":
        dungeon.pop_event()
        dungeon.state = GameState.INVENTORY_MANAGEMENT
      case _:
        raise GameActionError("Invalid Action")
