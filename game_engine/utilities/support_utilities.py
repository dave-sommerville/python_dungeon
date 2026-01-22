from .rng_utilities import random_integer
def get_rarity():
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

# @staticmethod
# # Oddly placed static function *****
# def get_current_menu(dungeon):
#     if dungeon.current_event:
#         return dungeon.current_event.get_options()

#     match dungeon.state:
#         case GameState.MAIN_MENU:
#             actions_list = dungeon.player.current_chamber.move_actions()
#             actions_list.extend(
#                 ["search", "rest", "inventory", "spells", "details", "describe"]
#             )
#             return actions_list
#         case GameState.INVENTORY_MANAGEMENT:
#             return dungeon.player.print_character_inventory()
#         case GameState.SPELL_MANAGEMENT:
#             return ["cast", "inspect", "back"]
#         case _:
#             raise GameActionError("Invalid Action")
