from item import Item
class Weapon(Item):
    damage = 0
    attack_bonus = 0
    range_of_attack = 0
    martial_weapon = False

    def __init__(self, name, durability, damage, attack_bonus, range_of_attack):
        super.__init__(name, durability)
        self.damage = damage
        self.attack_bonus = attack_bonus
        self.range_of_attack = range_of_attack
    
    