from ...utilities.desc_utitlities import base_item_description
from ...utilities.rng_utilities import random_integer

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.durability = 1
        self.cost = 5

    def use_item(self):
        return ('You cannot use this item')

    def item_description(self):
        return f"{self.name}: {self.description}"