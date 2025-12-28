import math
from .character import Character
from ...locations.chamber import Chamber
from ..items.item import Item
from ..items.potion import Potion
from ...game_action_error import GameActionError
from ...utilities.rng_utilities import weighted_decision
    # prisoner_status = ''

class Player(Character):
    """
    Outside of skill checks:
        Con: Increases MaxHP
        Dex: Increases AC
        Wis/Cha increases magic ability
        Cha improves likeability 
        Wis helps against being surprised
    """

    def __init__(self, name, description):
        super().__init__(name,description)
        # Character Statuses
        # self.is_dodging = False
        # self.is_stunned = False
        # self.is_poisoned = False

        # Player State Management
        self.message_buffer = []
        self.x = 0
        self.y = 0
        self.current_chamber = Chamber("0,0")
        # self.plot_progression = None

        # Player Base Upgrades
        self.modifer = 0 # super(): 0
        self.health = 80 # super(): 30
        self.maxHP = 100 # super(): 100
        self.armor_class = 10 # super(): 8
        
        self.killcount = 0
        self.exhaustion_counter = 0
        self.gold = 0
        self.mana = 5
        self.sanity = 100

        # Player Characteristics 
        self.player_level = 0
        self.xp = 0
        self.dex = 0
        self.con = 0
        self.cha = 0
        # self.wis = 0
        # self.stealth = 0

        # Item Management
        self.inventory = [Item("A cup", "Shiny", 10), Item("A Key", "Old", 2), Potion("Potion", "of healing", 20)]
        self.inventory_size = 5
        self.weapon_secondary = None
        self.magical_item = None

    def _msg(self, text):
        self.message_buffer.append(text)

    def print_player_info(self):
        return [
            f"Health: {self.health}/{self.maxHP} "
            f"Sanity: {self.sanity}",
            f"Mana: {self.mana} ",
            f"Exhaustion: {self.exhaustion_counter} "
            f"Gold: {self.gold} ",
            f"Killcount: {self.killcount} "
            f"Level: {self.player_level} XP: {self.xp} ",
            f"AC: {self.armor_class} "
        ]
    
    def build_player_from_stats(self):
        self.player_level = self.scaled_value(self.xp)
        self.health = 100 + ((self.player_level + self.con) * 10)

    def scaled_value(self, value):
        return max(0, int(math.log(value / 1000, 2)) + 1)

    def print_current_location(self):
        return f"{self.x},{self.y}"
    
    def print_next_location(self, direction):
        match direction:
            case "north":
                return f"{self.x + 1},{self.y}"
            case "east":
                return f"{self.x},{self.y + 1}"
            case "south":
                return f"{self.x - 1},{self.y}"
            case "west":
                return f"{self.x},{self.y - 1}"
            case _:
                raise ValueError(f"{direction} is not a valid direction.")

    def search_chamber(self):
        # Need to add perception mechanic
        # Need to add trap/contest mechanic
        loot_list = []
        loot_count = len(self.current_chamber.chamber_items)
        inventory_room = self.inventory_length - len(self.inventory)
        if loot_count > 0 and loot_count <= inventory_room:
            for item in self.current_chamber.chamber_items:
                loot_list.append(item.name)
                self.add_to_inventory(item)

    def print_character_inventory(self):
        """Return inventory entries WITHOUT numeric prefixes.

        The UI is responsible for adding 1-based numbering. This avoids
        duplicated numbers when the frontend also numbers options.
        """
        inventory_list = []
        for item in self.inventory:
            inventory_list.append(f"{item.name} - {item.durability}")
        inventory_list.append("back")
        return inventory_list

    # Will need to add limiting to list, but mayaswell enjoy the dynamic sizes for now
    def add_to_inventory(self, item):
        if len(self.inventory) >= self.inventory_size:
            raise GameActionError("Inventory is currently full")
        self.inventory.append(item)

    def exhaustion_check(self, dungeon):
        if weighted_decision(0.6):
            if self.exhaustion_counter > 6:
                self.health -= 5
                dungeon._msg("You are exhausted and lose some health from the activity.")
                # Player death check
            else:
                self.exhaustion_counter += 1
                dungeon._msg("You are feeling a little tired from all this activity")

    def add_skill_point(self, skill):
        match skill:
            case "dex":
                self.dex += 1
            case "con":
                self.con += 1
            case "cha": 
                self.cha += 1
            case "wis":
                self.wis += 1



