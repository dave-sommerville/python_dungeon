from .item import Item
from ...utilities.desc_utitlities import potion_description
from ...utilities.rng_utilities import random_integer

class Potion(Item):
    def __init__(self, name_or_rarity, description=None, value=None):
        # Support explicit (name, description, potency) or rarity-based construction
        if description is not None or value is not None:
            super().__init__(name_or_rarity, description, value)
            self.potency = value if value is not None else random_integer(1, 10)
        else:
            rarity = name_or_rarity
            super().__init__(rarity)
            info_obj = potion_description()
            self.name = info_obj[0]
            self.description = info_obj[1]
            self.potency = random_integer((rarity * 10), (rarity * 20))

    def use_item(self, character):
        character.health += self.potency
        if character.health > character.maxHP:
            character.health = character.maxHP