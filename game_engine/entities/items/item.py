from ...utilities.desc_utitlities import base_item_description
from ...utilities.rng_utilities import random_integer

class Item:
    def __init__(self, name_or_rarity, description=None, value=None):
        """Support two call styles:
        - Item(rarity) -> generates name/description via base_item_description
        - Item(name, description, value) -> explicit item
        """
        # Legacy explicit item signature
        if description is not None or value is not None:
            self.name = name_or_rarity
            self.description = description or ""
            self.durability = 1
            self.cost = value if value is not None else random_integer(1, 10)
        else:
            # Newer rarity-based generation
            rarity = name_or_rarity
            info_obj = base_item_description(rarity)
            self.name = info_obj[0]
            self.description = info_obj[1]
            self.durability = 1
            self.cost = random_integer(rarity, (rarity * 10))

    def use_item(self, character):
        return ('You cannot use this item')

    def item_description(self):
        return f"{self.name}: {self.description}"
    