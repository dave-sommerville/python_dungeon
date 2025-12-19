from .game_states import GameState
from .game_action_error import GameActionError
from .locations.dungeon import Dungeon
from .entities.characters.character import Character
from .events.combat import CombatEvent
from .events.inventory_item import InventoryItemEvent
from .utilities.rng_utilities import weighted_decision


class GameEngine:
    def __init__(self):
        self.logs = []
        self.error = None

    def resolve_action(self, dungeon, action: str):
        self.logs = []
        self.error = None
        try:
            # If there's a current event, resolve it first (event menus take precedence)
            if getattr(dungeon, 'current_event', None):
                self._resolve_event_action(dungeon, action)
            else:
                # Attempt the game logic for the current state
                self._resolve_state_action(dungeon, action)

        except GameActionError as e:
            # If an error happens, we catch it here
            self.error = str(e)
        finally:
            # This block runs NO MATTER WHAT (success or error)
            self.logs.extend(dungeon.message_buffer)
            dungeon.message_buffer = []
        return {
            "logs": self.logs,
            "menu": self.get_current_menu(dungeon),
            "error": self.error,
        }

    def _log(self, message):
        self.logs.append(message)

    def _resolve_event_action(self, dungeon, action):
        event = dungeon.current_event
        if not event:
            raise GameActionError("No active event to resolve")
        options = event.get_options() or []
        # Accept numeric selection or exact match; caller UI maps numbers, engine expects strings
        if action not in options:
            raise GameActionError("Invalid event option")
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
                raise GameActionError("Invalid State")

    def _call_for_combat_event(self, dungeon):
        if weighted_decision(0.5):
            character = Character("Jeff", "The Skeleton")
            event = CombatEvent(character)
            dungeon.current_event = event

    # Has to check the room's direction for sneaky players
    def _resolve_main_menu(self, dungeon, action):
        match action:
            case "move north":  # Sub events
                dungeon.move_player("north")
                self._call_for_combat_event(dungeon)
                self._log(dungeon.player.print_current_location())
            case "move east":  # Sub events
                dungeon.move_player("east")
                self._call_for_combat_event(dungeon)
                self._log(dungeon.player.print_current_location())
            case "move south":  # Sub events
                dungeon.move_player("south")
                self._call_for_combat_event(dungeon)
                self._log(dungeon.player.print_current_location())
            case "move west":  # Sub events
                dungeon.move_player("west")
                self._call_for_combat_event(dungeon)
                self._log(dungeon.player.print_current_location())
            case "search":
                dungeon.player.search_chamber()
            case "rest":
                dungeon.player.attempt_to_rest()
            case "inventory":
                dungeon.state = GameState.INVENTORY_MANAGEMENT
                self._log("Select item")
                pass
            case "spells":
                pass
            case "details":
                dungeon.log_player_info()
            case "describe":
                self._log(dungeon.describe_current_chamber())
            case _:
                raise GameActionError("Invalid Action")

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
                    self._log(item.item_description())
                    dungeon.current_event = InventoryItemEvent(item, index)
                    return
        raise GameActionError("Invalid input")

    def _resolve_spell_management_menu(self, dungeon, action):
        pass

    @staticmethod
    def get_current_menu(dungeon):
        if dungeon.current_event:
            return dungeon.current_event.get_options()

        match dungeon.state:
            case GameState.MAIN_MENU:
                actions_list = dungeon.player.current_chamber.move_actions()
                actions_list.extend(
                    ["search", "rest", "inventory", "spells", "details", "describe"]
                )
                return actions_list
            case GameState.INVENTORY_MANAGEMENT:
                return dungeon.player.print_player_inventory()
            case GameState.SPELL_MANAGEMENT:
                return ["cast", "inspect", "back"]
            case _:
                raise GameActionError("Invalid Action")