from .item import Item
from ...utilities.desc_utitlities import armor_description
from ...utilities.rng_utilities import random_integer

class Armor(Item):
    def __init__(self, rarity):
        super().__init__(rarity)
        info_obj = armor_description(rarity)
        self.name = info_obj[0]
        self.description = info_obj[1]

        self.ac_bonus = rarity + random_integer(1,3)
        self.dex_impairment = False
    
