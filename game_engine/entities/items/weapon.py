from item import Item
class Weapon(Item):

    def __init__(self, name, durability, damage, attack_bonus):
        super.__init__(name, durability)
        self.damage = damage
        self.attack_bonus = attack_bonus
        self.range_attack = False
        self.martial_weapon = False
    
    