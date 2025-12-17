from game_states import GameState
from locations.dungeon import Dungeon
from entities.characters.character import Character
from events.combat import CombatEvent
from events.inventory_item import InventoryItemEvent

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
        event.resolve(dungeon, action)

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
            
    def _call_for_combat_event(self, dungeon):
        character = Character("Jeff", "The Skeleton")
        event = CombatEvent(character)
        dungeon.current_event = event

    def _resolve_main_menu(self, dungeon, action):
        match action:
            case "move north": # Sub events
                dungeon.move_player("north")
                self._call_for_combat_event(dungeon)
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
                print("Select item")
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
        player = dungeon.player

        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            return

        # Extract leading number if present (e.g. "0: Sword")
        if ":" in action:
            index_part = action.split(":")[0]

            if index_part.isdigit():
                index = int(index_part)

                if 0 <= index < len(player.inventory):
                    item = player.inventory[index]
                    dungeon.current_event = InventoryItemEvent(item)
                    return

        print("Invalid input")



    def _resolve_spell_management_menu(self, dungeon, action):
        pass

    @staticmethod
    def get_current_menu(dungeon):
        if dungeon.current_event:
            return dungeon.current_event.get_options()

        match dungeon.state:
            case GameState.MAIN_MENU:
                actions_list = dungeon.player.current_chamber.move_actions()
                actions_list.extend(["search", "rest", "inventory", "spells", "details", "describe"])
                return actions_list
            case GameState.INVENTORY_MANAGEMENT:
                return dungeon.player.print_player_inventory()
            case GameState.SPELL_MANAGEMENT:
                return ["cast", "inspect", "back"]
            case _:
                return []
