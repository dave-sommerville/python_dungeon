from entities.entity import Entity
class Character(Entity):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.is_dodging = False
        self.is_stunned = False
        self.armor_class = 0
        self.inventory = []
        self.health = 0
        
    def some_method(self):
        pass
