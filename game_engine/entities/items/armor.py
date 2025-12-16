from item import Item
class Armor(Item):
    ac_bonus = 0
    dex_impairment = False

    def __init__(self, name, durability, ac_bonus, dex_impairment):
        super.__init__(name, durability)
        self.ac_bonus = ac_bonus
        self.dex_impairment = dex_impairment
    
