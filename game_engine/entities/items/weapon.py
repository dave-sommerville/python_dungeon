from .item import Item
from ...utilities.desc_utitlities import weapon_description
from ...utilities.rng_utilities import random_integer

class Weapon(Item):
    def __init__(self, name, description, damage, attack_bonus):
        super().__init__(name, description)
        self.damage = damage
        self.attack_bonus = attack_bonus
        self.range_attack = False
        self.martial_weapon = False
    
    