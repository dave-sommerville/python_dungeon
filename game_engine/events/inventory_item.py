from .event import Event

class InventoryItemEvent(Event):
  def __init__(self, entity):
    super().__init__(entity)
  def get_options(self):
    return ["use", "discard", "back"]

  def resolve(self, dungeon, action):
    match action:
      case "use":
        self.entity.use_item()
        dungeon.player.inventory.remove(self.entity)
        dungeon.current_event = None
      case "discard":
        dungeon.player.inventory.remove(self.entity)
        print("Item Removed")
        dungeon.player.print_inventory()
        dungeon.current_event = None
      case "back":
        dungeon.current_event = None
      case _:
        return