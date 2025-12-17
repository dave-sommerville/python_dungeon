class Item:
    name = ''
    description = ''
    durability = 10
    def __init__(self, name, description, durability):
        self.name = name
        self.description = description
        self.durability = durability
    def use_item(self):
        # Mostly for durability, except in potions
        print('You cannot use this item')
    def display_description(self):
        print(self.description)