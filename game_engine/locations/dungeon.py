from ..entities.characters.player import Player
from .chamber import Chamber
from ..game_states import GameState
from ..utilities.rng_utilities import weighted_decision


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

    def create_player(self):
        pass

    def move_player(self, direction):
        self._msg(f"You move {direction}")
        # Determine target chamber before describing it
        next_id = self.player.print_next_location(direction)
        t_x, t_y = map(int, next_id.split(','))

        next_chamber = next((c for c in self.visited_locations if c.id == next_id), None)

        if not next_chamber:
            next_chamber = Chamber(next_id)
            next_chamber.add_reverse_passage(self.reverse_direction(direction))
            self.visited_locations.append(next_chamber)

        if weighted_decision(0.6):
            self.player.exhaustion_counter += 1

        self.player.current_chamber = next_chamber
        self.player.x = t_x
        self.player.y = t_y
        # Describe the new chamber
        self._msg(f"As you look around, you see {self.describe_current_chamber()}")

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

    def log_player_info(self):
        player_info_list = self.player.print_player_info()
        for info in player_info_list:
            self._msg(info)

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

    def create_map(self):
        pass

    def display_map(self):
        pass
