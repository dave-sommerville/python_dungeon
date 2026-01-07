from .item import Item
from ...utilities.desc_utitlities import potion_description
from ...utilities.rng_utilities import random_integer

class Potion(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.potency = random_integer(1, 10)

    def use_item(self, character):
        character.health += self.potency
        if character.health > character.maxHP:
            character.health = character.maxHP