from entities.characters.player import Player
# Content
    # Room descriptions
    # Passageway

# Non-State Actions
    # View Details (Not a state I don't think)
    #(Event Triggers possible)
    # Move
    # Search
    # Rest    

class Dungeon:
    player = None
    visited_locations  = []
    current_event = None

    def __init__(self):
        pass

    def create_player():
        pass
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
