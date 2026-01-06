from ..entities.characters.player import Player
from ..entities.characters.npc import NPC
from ..utilities.desc_utitlities import chamber_description
from .chamber import Chamber
from ..entities.characters.character import Character
from ..events.combat import CombatEvent
from ..game_states import GameState
from ..utilities.rng_utilities import random_integer, weighted_decision, random_list_element
from ..entities.items.item import Item
from ..entities.items.armor import Armor
from ..entities.items.potion import Potion
from ..entities.items.weapon import Weapon

class Dungeon:
    current_event = None
    state = GameState.MAIN_MENU

    def __init__(self):
        self.message_buffer = []
        self.player = Player("Gal", "Guy")
        # Track visited chambers (start with player's initial chamber)
        self.visited_locations = [self.player.current_chamber]
        self.current_event = None

    def _msg(self, text):
        self.message_buffer.append(text)

    def name_player(self, name):
        self.player.name = name

    def describe_player(self, description):
        self.player.description - description

    def create_player(self):
        pass
    
    def move_player(self, direction):
        if direction == "north" and not self.player.current_chamber.north_passage:
            print("blocked")
            return
        if direction == "east" and not self.player.current_chamber.east_passage:
            print("blocked")
            return
        if direction == "south" and not self.player.current_chamber.south_passage:
            print("blocked")
            return
        if direction == "west" and not self.player.current_chamber.west_passage:
            print("blocked")
            return   
        self._msg(f"You move {direction}")
        # Determine target chamber before describing it
        next_id = self.player.print_next_location(direction)
        t_x, t_y = map(int, next_id.split(','))

        next_chamber = next((c for c in self.visited_locations if c.id == next_id), None)

        if not next_chamber:
            next_chamber = self.generate_chamber(next_id)
            next_chamber.add_reverse_passage(self.reverse_direction(direction))
            self.visited_locations.append(next_chamber)

        if weighted_decision(0.6):
            self.player.exhaustion_counter += 1

        self.player.current_chamber = next_chamber
        self.player.x = t_x
        self.player.y = t_y
        # Describe the new chamber
        self._msg(f"{self.describe_current_chamber()}")
        self._msg(f"What do you do next?")
        self._msg("")

    def generate_chamber(self, next_id):
        description = chamber_description()
        loot = self.generate_items()
        return Chamber(next_id, description, loot)
    
    def attempt_to_rest(self):
        # Need to add surprise combat mechanic
        if weighted_decision(0.2):
            character = Character("Jeff", "The Skeleton")
            self._msg(f"Before you can rest, you are {character.name}")
            event = CombatEvent(character)
            self.current_event = event
            return False
            pass
        else:
            self.player.exhaustion_counter = 0
            self._msg("You manage to rest safely and feel much better")
            return True
    # Conversion Function *****
    def get_rarity(self):
        index = random_integer(1, 100)
        if index > 95:
            return 10
        elif index > 85:
            return 8
        elif index > 70:
            return 7
        elif index > 50:
            return 5
        elif index > 20:
            return 3
        else:
            return 1
        
    def generate_items(self):
        loot = []
        if weighted_decision(0.2):
            loot.append(Weapon(self.get_rarity()))
            if weighted_decision(0.1):
                loot.append(Weapon(self.get_rarity()))
        if weighted_decision(0.5):
            loot.append(Armor(self.get_rarity()))
            if weighted_decision(0.1):
                loot.append(Weapon(self.get_rarity()))
        if weighted_decision(0.1):
            loot.append(Item(self.get_rarity()))
            if weighted_decision(0.1):
                loot.append(Weapon(self.get_rarity()))
        if weighted_decision(0.1):
            loot.append(Potion(self.get_rarity()))
            if weighted_decision(0.2):
                loot.append(Weapon(self.get_rarity()))
        return loot
    
    def generate_merchant(self):
        merchant = NPC("Jeff"," the Merchant")
        merchant.inventory.extend(self.generate_items())
        merchant.is_merchant = True
        return merchant

    def describe_current_chamber(self):
        """Return the description for the chamber the player is currently in.

        Looks up the chamber by id in visited_locations (which stores Chamber objects
        with string ids like "x,y"). If not found, falls back to the player's
        current_chamber and ensures it's tracked.
        """
        location_id = self.player.print_current_location()
        chamber = next((c for c in self.visited_locations if c.id == location_id), None)
        if chamber:
            return chamber.description
        # Fallback to player's current chamber (and track it for future lookups)
        if getattr(self.player, "current_chamber", None):
            self.visited_locations.append(self.player.current_chamber)
            return self.player.current_chamber.description
        return "You see nothing of interest."
    
    @staticmethod
    def reverse_direction(direction):
        match direction:
            case "north":
                return "south"
            case "east":
                return "west"
            case "south":
                return "north"
            case "west":
                return "east"
            case _:
                raise ValueError("Invalid direction")

    def display_player_inventory(self):
        for item in self.player.inventory:
            self._msg(f"{item}")


