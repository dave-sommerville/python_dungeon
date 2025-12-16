from character import Character
    # prisoner_status = ''

class Player(Character):
    # Basic
    name = ''
    description = ''
    killcount = 0
    x = 0
    y = 0
    current_chamber = None
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
    weapon_primary = None
    weapon_secondary = None
    armor = None
    magical_item = None


    def __init__(self, name, description):
        super().__init__(name, description)
        self.health = 100
    def print_player_info(self):
        pass

    # This should print to bottom menu
    def print_player_inventory():
        pass
    def move_player():
        pass
    
    def search_chamber():
        pass
    def attempt_to_rest():
        pass
    

    # Manage inventory
    # Manage Spells
    #   
    #