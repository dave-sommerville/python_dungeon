from events.event import Event

class InventoryItemEvent(Event):
  def __init__(self, param):
    super().__init__(param)
  def get_options():
    return ["use", "discard", "back"]

  def resolve(self, action, dungeon):
    item = dungeon.player.inventory[self.param]
    match action:
      case "use":
        item.use_item()
      case "discard":
        dungeon.player.inventory.remove(item)
      case "back":
        dungeon.current_event = None
      case _:
        return