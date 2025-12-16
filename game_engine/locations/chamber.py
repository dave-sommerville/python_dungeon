# ChamberID
# Distribution property

class Chamber():
    id = ''
    description = ''
    chamber_items = []
    chamber_gold = 0
    north_passage = True
    east_passage = True
    south_passage = True
    west_passage = True

    def __init__(self, id):
        self.id = id
    def describe_chamber(self):
        return 'This'
