from entities.characters.player import Player
from locations.chamber import Chamber
# Content
    # Room descriptions
    # Passageway

class Dungeon:
    player = Player()
    visited_locations  = []
    current_event = None
    state = 'INIALIZING'


    def __init__(self):
        pass

    def create_player():
        pass
    # Needs Directions, chance of encounter,
    # Moving:
        # Randomize passages
        # Add return passage
        # Display only present passages
    def move_player(self):
        next_id = self.player.print_next_location()
        next_chamber = next((chamber for chamber in self.visited_locations if chamber.id == next_id), None)
        if next_chamber:
            self.player.current_chamber = next_chamber
        else:
            next_chamber = Chamber(next_id)
            self.player.current_chamber = next_chamber
            self.visited_locations.append(next_chamber)
            self.player.x += 1
            self.player.exhaustion_counter += 1

    def transfer_data():
        pass
    def create_map():
        pass
    def display_map():
        pass

"""
Persistent Info Displayed:
    HP
    Sanity
    Location
STATES
Initializing (Event instead of menu)
Main Menu:
    Move
    Rest
    Search
    Manage Inventory
    Manage Spells
    Show Player details
    Describe Room Again
    Exit Game
Inventory Management:
    Auto prints to bottom screen
    Use
    Discard
    Return

EVENT STATES    
Combat:
    Attack (depending on attacks available)
    Attempt to speak
    Cast a preppared spell
    Dodge
    Retreat
Skill Check:
    Dodge attack (Dex)
    Break open door (Con)
    Pick Lock (Dex)
    Dodge Area damage (Dex)
    Ingest poison (Con)
    Tell a lie (Cha)
    Ask for help (Cha)
    Search room (Wis)
    Examine lore (Wis)
NPC Interaction:

Merchant:

Levelling Up:


"""
"""
EVENT TRIGGERS
    Move
        Interaction
        Combat
        Skill Check
    Search
        Skill Check
    Rest
        Combat
"""
