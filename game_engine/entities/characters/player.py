from entities.characters.character import Character
from locations.chamber import Chamber
    # prisoner_status = ''

class Player(Character):
    # Basic
    name = ''
    description = ''
    killcount = 0
    x = 0
    y = 0
    current_chamber = Chamber("00")
    # plot_progression = None

    # Stats
    player_level = 1
    modifer = 0
    maxHP = 0
    armor_class = 10
    dex = 0
    con = 0
    cha = 0
    wis = 0
    """
    Outside of skill checks:
        Con: Increases MaxHP
        Dex: Increases AC
        Wis/Cha increases magic ability
        Cha improves likeability 
        Wis helps against being surprised
    """

    xp = 0
    exhaustion_counter = 0
    gold = 0
    mana = 5
    sanity = 100
    inventory = []
    inventory_size = 5
    weapon_primary = None
    weapon_secondary = None
    armor = None
    magical_item = None


    def __init__(self):
        super().__init__()
        self.health = 100

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

