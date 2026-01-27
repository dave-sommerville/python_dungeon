from .chamber import Chamber
from ..entities.characters.player import Player
from ..entities.characters.character import Character
from ..events.inventory.inventory_management import InventoryManagementEvent
from ..events.combat.combat import CombatEvent
from ..utilities.desc_utitlities import chamber_description
from ..utilities.rng_utilities import random_integer, weighted_decision, random_list_element
from ..utilities.support_utilities import reverse_direction, get_rarity
from ..game_states import GameState
from ..factory import random_item_factory

class Dungeon:
    current_event = None
    state = GameState.MAIN_MENU

    def __init__(self):
        self.message_buffer = []
        self.player = Player("Gal", "Guy")
        # Track visited chambers (start with player's initial chamber)
        self.visited_locations = [self.player.current_chamber]
        self.event_stack = []  # Stack for managing event transitions
    
    @property
    def current_event(self):
        """Get the current event from the top of the stack."""
        return self.event_stack[-1] if self.event_stack else None
    
    @current_event.setter
    def current_event(self, event):
        """Set the current event. For backward compatibility, replaces the entire stack if provided."""
        if event is None:
            self.event_stack = []
        else:
            self.event_stack = [event]
    
    def push_event(self, event):
        """Push a new event onto the event stack."""
        self.event_stack.append(event)
    
    def pop_event(self):
        """Pop the current event from the stack and return it."""
        if self.event_stack:
            return self.event_stack.pop()
        return None
    
    def peek_event(self):
        """Peek at the current event without removing it."""
        return self.current_event
    def _msg(self, text):
        self.message_buffer.append(text)
    
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
            next_chamber.add_reverse_passage(reverse_direction(direction))
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
        chamber = Chamber(next_id, description, loot)
        chamber.establish_passageways()
        return chamber
    
    def attempt_to_rest(self):
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
        
    def generate_items(self):
        loot = []
        amount = random_integer(1,4)
        for i in range(amount):
            loot.append(random_item_factory(get_rarity()))
        return loot
    
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
    
    def display_player_inventory(self):
        for item in self.player.inventory:
            self._msg(f"{item}")

    def search_chamber(self):
        search_dc = random_integer(2,7)
        loot_list = []
        loot_count = len(self.player.current_chamber.chamber_items)
        inventory_room = self.player.get_inventory_room()
        if self.player.wis < search_dc or loot_count <= 0:
            loot_list.append("Nothing is found in this chamber")
        else:
            if loot_count <= inventory_room:
                loot_list.append(f"You find {loot_count} items:")
                for item in self.player.current_chamber.chamber_items:
                    loot_list.append(item.name)
                    self.player.add_to_inventory(item)
            else:
                loot_list.append("You have found some items but your inventory is full")
                loot_list.append(f"You need to discard {loot_count - inventory_room} item(s) to pick up the found items")
                # Create loot bag with all items (found + inventory) and track which are found
                all_items = list(self.player.current_chamber.chamber_items)
                all_items.extend(self.player.inventory)
                self.push_event(InventoryManagementEvent(self.player, mode="discard", items_list=all_items))
        return loot_list