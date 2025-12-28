from ..entity import Entity
from ...utilities.rng_utilities import random_integer, weighted_decision
from ..items.weapon import Weapon
class Character(Entity):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.is_dodging = False
        self.is_stunned = False
        self.is_poisoned = False
        self.modifer = 0
        self.health = 70
        self.maxHP = 100
        self.armor_class = 8
        self.weapon_primary = Weapon(2)
        self.stealth = 0
        self.wis = 0
        self.inventory = []
        self.xp_award = 5
        # self.armor = None
        
    def don_armor(self, armor):
        pass
    def doff_armor(self):
        pass
    def attack_action(self, character):
        attack  = self.modifer + random_integer(2,8)
        damage = random_integer(10, 30)
        if self.weapon_primary:
            attack += self.weapon_primary.attack_bonus
            damage += self.weapon_primary.damage
        target = character.armor_class
        if character.is_dodging:
            target *= 2
            character.is_dodging = False
        if attack > target:
            character.health -= damage
            return damage
        else:
            return 0

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

    def print_character_inventory(self):
        """Return inventory entries WITHOUT numeric prefixes.
        The UI is responsible for adding 1-based numbering. This avoids
        duplicated numbers when the frontend also numbers options.
        """
        inventory_list = []
        for item in self.inventory:
            inventory_list.append(f"{item.name} - {item.durability}")
        inventory_list.append("back")
        return inventory_list
