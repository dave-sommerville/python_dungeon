from .event import Event
from ..game_states import GameState

class MerchantEvent(Event):
  def __init__(self, entity, index):
    super().__init__(entity)
    self.index = index
  def get_options(self):
    return ["purchase", "back"]
  def resolve(self, dungeon, action):
      match action:
          case "use":
              self.entity.use_item(dungeon.player)
              del dungeon.player.inventory[self.index]
              dungeon.message_buffer.append("Item purchased.")
              dungeon.current_event = None

          case "back":
              dungeon.current_event = None

