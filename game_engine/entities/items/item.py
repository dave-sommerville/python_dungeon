from ...utilities.desc_utitlities import base_item_description
from ...utilities.rng_utilities import random_integer

class Item:
    def __init__(self, rarity):
        info_obj = base_item_description(rarity)
        self.name = info_obj[0]
        self.description = info_obj[1]
        durability = 1
        self.durability = durability
        self.cost = random_integer(rarity,(rarity * 10))

    def use_item(self, character):
        return ('You cannot use this item')

    def item_description(self):
        return f"{self.name}: {self.description}"
    