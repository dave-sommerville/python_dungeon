from items.item import Item
from entities.characters.player import Player
class Potion():
    def __init__(self, name, description, type_of_potion, potency):
        super().__init__(name, description, durability=1)
        self.type_of_potion = type_of_potion
        self.potency = potency
    def use_item(self, character):
        match self.type_of_potion:
            case "healing":
                character.heal(self.potency)
                self.durability = 0
            case "damage":
                character.health -= self.potency
                self.durability = 0
            case "restoration":
                if isinstance(character, Player):
                    if self.potency >= 5:
                        character.health = character.maxHP
                        character.exhaustion
                        character.mana += 5
                    else:
                        character.heal(50)
                else:
                    character.heal(50)
                self.durability = 0
            case _:
                print("Invalid type")