from ..entity import Entity
from ...utilities.rng_utilities import random_integer, weighted_decision
class Character(Entity):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.is_dodging = False
        self.is_stunned = False
        self.modifer = 0
        self.armor_class = 10
        self.inventory = []
        self.health = 30
        self.weapon_primary = None
        self.armor = None
        self.maxHP = 30
        
    def don_armor(self, armor):
        pass
    def doff_armor(self):
        pass
    def attack_action(self, character):
        print("you attack")
        attack  = self.modifer + random_integer(2,8)
        damage = random_integer(10, 30)
        if self.weapon_primary:
            attack_modifer += self.weapon_primary.attack_bonus
            damage + self.weapon_primary.damage
        target = character.armor_class
        if character.is_dodging:
            target *= 2
            character.is_dodging = False
        if attack > target:
            character.health -= damage
            print("You hit")
        else:
            print("You missed")

    def dodge_action(self):
        self.is_dodging = True

    def character_death_check(self):
        if self.health <= 0:
            return True
        else:
            return False
        
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHP:
            self.health = self.maxHP
