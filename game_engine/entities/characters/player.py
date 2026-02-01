import math
from .character import Character
from ...entities.spells.spellbook import SpellBook
from ...entities.spells.spell import Spell
from ...locations.chamber import Chamber
from ..items.item import Item
from ..items.potion import Potion
from ...errors.game_action_error import GameActionError
from ...utilities.rng_utilities import weighted_decision, random_list_element, random_integer
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
        self.health = 80 # super(): 70
        self.maxHP = 100 # super(): 100
        self.armor_class = 10 # super(): 8
        self.combat_round = None
        
        self.killcount = 0
        self.exhaustion_counter = 0
        self.gold = 0
        self.mana = 5
        self.sanity = 100

        # Player Characteristics 
        self.player_level = 0
        self.xp = 0
        self.dex = 5
        self.con = 5
        # self.cha = 5
        # self.wis = 5
        # self.stealth = 0

        # Item Management
        self.inventory = [Potion("Potion", "of healing")]
        self.inventory_size = 2
        self.weapon_secondary = None
        self.magical_item = None
        self.known_spells = [Spell("Healing", "Spell of healing", SpellBook.shield, 2, 2)]

    def print_character_info(self):
        return [
            f"AC: {self.armor_class} - "
            f"Health: {self.health}/{self.maxHP} ",
            f"Sanity: {self.sanity}", # Take this out for release
            f"Mana: {self.mana} ", 
            f"Exhaustion: {self.exhaustion_counter} " 
            f"Gold: {self.gold} ",
            f"Killcount: {self.killcount} "
            f"Level: {self.player_level} XP: {self.xp} ",
            f"Location: {self.y}, {self.x}"
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
    def get_possible_player_moves(self):
        move_list = []
        if self.current_chamber.north_passage:
            move_list.append("north")
        if self.current_chamber.east_passage:
            move_list.append("east")
        if self.current_chamber.south_passage:
            move_list.append("south")
        if self.current_chamber.west_passage:
            move_list.append("west")
        return random_list_element(move_list)

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
    def get_inventory_room(self):
        return self.inventory_size - len(self.inventory)
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
    
    def full_restore_self(self):
        super().full_restore_self()
        self.mana += 5
        self.exhaustion_counter = 0



