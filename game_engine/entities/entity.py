
class Entity():
    _next_id = 1

    def __init__(self, name, description):
        self.id = Entity._next_id
        Entity._next_id += 1
        self.name = name
        self.description = description
        
