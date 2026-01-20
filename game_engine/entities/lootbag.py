from ..entities.entity import Entity
class LootBag(Entity):
    def __init__(self,loot_items):
        super().__init__("lootbag", "Too much loot")
        self.loot_items = loot_items
        