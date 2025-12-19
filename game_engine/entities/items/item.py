class Item:
    name = ''
    description = ''
    durability = 10
    def __init__(self, name, description, durability):
        self.name = name
        self.description = description
        self.durability = durability
    def use_item(self, character):
        return ('You cannot use this item')

    def item_description(self):
        return f"{self.name}: {self.description}"
    