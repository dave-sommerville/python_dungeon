from game_states import GameState
from locations.dungeon import Dungeon
class GameEngine:
    def resolve_action(self, dungeon, action: str):
        if dungeon.current_event:
            self._resolve_event_action(dungeon, action)
        else:
            self._resolve_state_action(dungeon, action)

    def _resolve_event_action(self, dungeon, action):
        event = dungeon.current_event
        options = event.get_options()
        if action not in options:
            print("Not a valid option ")
        event.resolve(action, dungeon)


    def _resolve_state_action(self, dungeon, action):
        match dungeon.state:
            case GameState.MAIN_MENU:
                self._resolve_main_menu(dungeon, action)
            case GameState.INVENTORY_MANAGEMENT:
                self._resolve_inventory_management_menu(dungeon, action)
            case GameState.SPELL_MANAGEMENT:
                self._resolve_spell_management_menu(dungeon, action)
            case _:
                print("Invalid State")
                return
    
    def _resolve_main_menu(self, dungeon, action):
        match action:
            case "move north": # Sub events
                dungeon.move_player("north")
                print(dungeon.player.print_current_location())
            case "move east": # Sub events
                dungeon.move_player("east")
                print(dungeon.player.print_current_location())
            case "move south": # Sub events
                dungeon.move_player("south")
                print(dungeon.player.print_current_location())
            case "move west": # Sub events
                dungeon.move_player("west")
                print(dungeon.player.print_current_location())
            case "search":
                dungeon.player.search_chamber()
            case "rest":
                dungeon.player.attempt_to_rest()
            case "inventory":
                dungeon.state = GameState.INVENTORY_MANAGEMENT
                dungeon.player.print_inventory()
                pass
            case "spells":
                pass
            case "details":
                details = dungeon.player.print_player_info()
                print(details)
            case "describe":
                roomDesc = dungeon.player.current_chamber.describe_chamber()
                print(roomDesc)
            case _:
                print("Invalid Action")
                return
    
    def _resolve_inventory_management_menu(self, dungeon, action):
        match action:
            case "back":
                dungeon.state = GameState.MAIN_MENU
            case _:
                print("invalid input")
                return

    def _resolve_spell_management_menu(self, dungeon, action):
        pass
    @staticmethod
    def get_current_menu(dungeon):
        if dungeon.current_event:
            return dungeon.current_event.get_options()

        match dungeon.state:
            case GameState.MAIN_MENU:
                actions_list = dungeon.player.current_chamber.move_actions()
                actions_list.append("search", "rest", "inventory", "spells", "details", "describe")
                return actions_list
            case GameState.INVENTORY_MANAGEMENT:
                return ["use", "equip", "drop", "back"]
            case GameState.SPELL_MANAGEMENT:
                return ["cast", "inspect", "back"]
            case _:
                return []
