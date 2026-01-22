# ChamberID
# Distribution property
from ..entities.items.item import Item
from ..utilities.rng_utilities import weighted_decision, random_integer
from ..utilities.desc_utitlities import passageway_descriptions
class Chamber():

    def __init__(self, id, description="", chamber_items=None):
        self.id = id
        # ensure each chamber gets its own list
        if chamber_items is None:
            chamber_items = []
        self.chamber_items = chamber_items
        self.description = description
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
    
    def establish_passageways(self):
        room_description = self.description
        if self.north_passage:
            room_description += f"To the North {passageway_descriptions()}" 
        if self.east_passage:
            room_description += f"To the East {passageway_descriptions()}"
        if self.south_passage:
            room_description += f"To the South {passageway_descriptions()}"
        if self.west_passage:
            room_description += f"To the West {passageway_descriptions()}"
        self.description = room_description