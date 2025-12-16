class Item:
    name = ''
    durability = 10
    def __init__(self, name, durability):
        self.name = name
        self.durability = durability
    def use_item(self):
        # Mostly for durability, except in potions
        print('You cannot use this item')
