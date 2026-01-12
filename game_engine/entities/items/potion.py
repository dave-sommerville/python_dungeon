from .item import Item
from ...utilities.desc_utitlities import potion_description
from ...utilities.rng_utilities import random_integer

class Potion(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.potency = random_integer(1, 10)

    def use_item(self, character):
        if self.potency < 3:
            hp_amount = random_integer(10,30)
            character.heal_self(hp_amount)
        elif self.potency < 8:
            hp_amount = random_integer(25,50)
            character.heal_self(hp_amount)
        else:
            character.full_restore_self()

