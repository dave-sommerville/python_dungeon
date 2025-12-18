from entities.characters.player import Player
from locations.chamber import Chamber
from game_states import GameState
from utilities.rng_utilities import weighted_decision
# Content
    # Room descriptions
    # Passageway

class Dungeon:
    current_event = None
    state = GameState.MAIN_MENU


    def __init__(self):
        self.message_buffer = []
        self.player = Player("Gal","Guy")
        self.visited_locations  = []
        self.current_event = None
    def _msg(self, text):
        self.message_buffer.extend(self.player.message_buffer)
        self.player.message_buffer = []
        self.message_buffer.append(text)

    def create_player(self):
        pass
    # Needs chance of encounter
    def move_player(self, direction):
        next_id = self.player.print_next_location(direction)
        t_x, t_y = map(int, next_id.split(','))

        next_chamber = next(
            (c for c in self.visited_locations if c.id == next_id),
            None
        )

        if not next_chamber:
            next_chamber = Chamber(next_id)
            next_chamber.add_reverse_passage(self.reverse_direction(direction))
            self.visited_locations.append(next_chamber)

            if weighted_decision(0.6):
                self.player.exhaustion_counter += 1

        self.player.current_chamber = next_chamber
        self.player.x = t_x
        self.player.y = t_y
    
    @staticmethod
    def reverse_direction(direction):
        match direction:
            case "north": return "south"
            case "east": return "west"
            case "south": return "north"
            case "west": return "east"
            case _: raise ValueError("Invalid direction")    
    
    def display_player_inventory(self):
        for i, item in enumerate(self.player.inventory, start=1):
            self._msg(f"{i}: {item}") # Change to response object

    def create_map(self):
        pass
    def display_map(self):
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
