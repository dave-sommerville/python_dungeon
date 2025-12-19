

class Item:
    def __init__(self, name, description, durability):
        self.name = name
        self.description = description
        self.durability = durability
        self.cost = 10

    def assign_properties(self, rarity):
        pass

    def use_item(self, character):
        return ('You cannot use this item')

    def item_description(self):
        return f"{self.name}: {self.description}"
    