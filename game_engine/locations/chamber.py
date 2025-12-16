# ChamberID
# Distribution property
from entities.items.item import Item
class Chamber():
    id = ''
    description = ''
    chamber_items = [Item("A pot", 10)]
    chamber_gold = 0
    north_passage = True
    east_passage = True
    south_passage = True
    west_passage = True

    def __init__(self, id):
        self.id = id
    def describe_chamber(self):
        return 'This'
