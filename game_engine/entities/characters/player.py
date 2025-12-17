from entities.characters.character import Character
from locations.chamber import Chamber
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
        self.health = 100
        self.killcount = 0
        self.x = 0
        self.y = 0
        self.current_chamber = Chamber("0,0")
        # self.plot_progression = None

        # Stats
        self.player_level = 1
        self.modifer = 0
        self.maxHP = 0
        self.armor_class = 10
        self.dex = 0
        self.con = 0
        self.cha = 0
        self.wis = 0
        # Resources 
        self.xp = 0
        self.exhaustion_counter = 0
        self.gold = 0
        self.mana = 5
        self.sanity = 100
        self.inventory = []
        self.inventory_size = 5
        self.weapon_primary = None
        self.weapon_secondary = None
        self.armor = None
        self.magical_item = None
    def print_player_info(self):
        print(f"{self.health}{self.sanity}{self.name}{self.killcount}")
        #Name, desc, killcount, location, level, xp, mod, maxHP
        # Current HP, AC (with armor), current weapon(s),
        # Gold, Mana, sanity, exhaustion
        pass

    # This should print to bottom menu
    def print_player_inventory(self):
        for i, item in enumerate(self.inventory):
            print(f"{i}: {item.name} - {item.durability}")
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
                print("invalid entry")
                return

    def search_chamber(self):
        # Need to add perception mechanic
        # Need to add trap/contest mechanic
        if len(self.current_chamber.chamber_items) > 0:
            for item in self.current_chamber.chamber_items:
                self.add_to_inventory(item)
        self.print_inventory()

    def attempt_to_rest(self):
        # Need to add surprise combat mechanic
        self.exhaustion_counter = 0
        print(self.exhaustion_counter)
    # Will need to add limiting to list, but mayaswell enjoy the dynamic sizes for now
    def add_to_inventory(self, item):
        self.inventory.append(item)
    def print_inventory(self):
        for item in self.inventory:
            print(item)
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
    # Manage inventory
    # Manage Spells

