from .event import Event
from ..game_states import GameState

class InventoryItemEvent(Event):
  def __init__(self, entity, index):
    super().__init__(entity)
    self.index = index
  def get_options(self):
    return ["use", "discard", "back"]
  def resolve(self, dungeon, action):
      match action:
          case "use":
              self.entity.use_item(dungeon.player)
              del dungeon.player.inventory[self.index]
              dungeon.message_buffer.append("Item used.")
              dungeon.current_event = None
              dungeon.state = GameState.MAIN_MENU

          case "discard":
              del dungeon.player.inventory[self.index]
              dungeon.message_buffer.append("Item discarded.")
              dungeon.current_event = None
              dungeon.state = GameState.MAIN_MENU

          case "back":
              dungeon.current_event = None
              dungeon.state = GameState.MAIN_MENU
