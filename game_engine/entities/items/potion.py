from .item import Item


class Potion(Item):
    def __init__(self, name, description, potency):
        super().__init__(name, description, durability=1)
        self.potency = potency
    def use_item(self, character):
        character.health += self.potency
        if character.health > character.maxHP:
            character.health = character.maxHP