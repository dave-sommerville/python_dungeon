from .item import Item
from ...utilities.desc_utitlities import armor_description
from ...utilities.rng_utilities import random_integer

class Armor(Item):
    def __init__(self, name, description, ac_bonus):
        super().__init__(name, description)
        self.name = name
        self.description = description
        self.ac_bonus = ac_bonus
        self.dex_impairment = False
    
