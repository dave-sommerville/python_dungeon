from item import Item
from ...utilities.desc_utitlities import weapon_description
from ...utilities.rng_utilities import random_integer

class Weapon(Item):
    def __init__(self, rarity):
        super.__init__(rarity)
        info_obj = weapon_description(rarity)
        self.name = info_obj[0]
        self.description = info_obj[1]

        self.damage = random_integer(rarity,(rarity * 10))
        self.attack_bonus = random_integer(rarity,(rarity * 10))
        self.range_attack = False
        self.martial_weapon = False
    
    