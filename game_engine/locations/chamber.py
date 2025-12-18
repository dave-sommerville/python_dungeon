# ChamberID
# Distribution property
from ..entities.items.item import Item
from ..utilities.rng_utilities import weighted_decision, random_integer
class Chamber():
    item = Item("Shiny", "A pot", 10)

    def __init__(self, id):
        self.id = id
        self.chamber_items = []
        self.chamber_items.append(Chamber.item)
        self.description = ''
        self.chamber_gold = random_integer(0, 50)
        self.north_passage = weighted_decision(0.7)
        self.east_passage = weighted_decision(0.6)
        self.south_passage = weighted_decision(0.6)
        self.west_passage = weighted_decision(0.6)


    def add_reverse_passage(self, direction):
        match direction:
            case "north":
                self.north_passage = True
            case "east":
                self.east_passage = True
            case "south":
                self.south_passage = True
            case "west":
                self.west_passage = True

    def describe_chamber(self):
        return 'This'
    
    def move_actions(self):
        actions_list = []
        if self.north_passage:
            actions_list.append("move north")
        if self.east_passage:
            actions_list.append("move east")
        if self.south_passage:
            actions_list.append("move south")
        if self.west_passage:
            actions_list.append("move west")
        return actions_list