from .events.inventory_management import InventoryManagementEvent
from .game_states import GameState
from .errors.game_action_error import GameActionError
from .events.combat import CombatEvent
from .events.npcs.merchant_interaction import MerchantEvent
from .utilities.rng_utilities import weighted_decision
from .factory import enemy_factory, merchant_factory, trap_factory
# Use a stack to hold events instead of referring to them within the object
# Leave main menu as the only resolution in the engine
# Instead of switching between states, only switch between numeric and string values
# Will have to consider all log effects to see the best architecture
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
            self.error = str(e)
        finally:
            self._game_over_check(dungeon)
            dungeon.message_buffer.extend(self.logs)
        return {
            "logs": self.logs,
            "menu": self.get_current_menu(dungeon),
            "error": self.error,
            "state": getattr(dungeon, 'state', None).name if getattr(dungeon, 'state', None) is not None else None,
            "event": getattr(dungeon, 'current_event', None) is not None,
        }

    def _log(self, message):
        self.logs.append(message)

    def _resolve_event_action(self, dungeon, action):
        event = dungeon.current_event
        if not event:
            raise GameActionError("No active event to resolve")
        options = event.get_options() or []
        # Accept numeric selection or exact match; caller UI maps numbers, engine expects strings
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
            # case GameState.INVENTORY_MANAGEMENT:
            #     return dungeon.player.print_character_inventory()
            # case GameState.SPELL_MANAGEMENT:
            #     return ["cast", "inspect", "back"]
            case _:
                raise GameActionError("Invalid Action")

    def _resolve_main_menu(self, dungeon, action):
        match action:
            case "move north":  # Sub events
                dungeon.move_player("north")
                self._call_for_combat_event(dungeon)
            case "move east":  # Sub events
                dungeon.move_player("east")
                self._call_for_merchant_event(dungeon)
            case "move south":  # Sub events
                dungeon.move_player("south")
                self._call_for_combat_event(dungeon)
            case "move west":  # Sub events
                dungeon.move_player("west")
                self._call_for_contest(dungeon)
            case "search":
                loot_list = dungeon.search_chamber()
                for item in loot_list:
                    dungeon._msg(item)
            case "rest":
                dungeon.attempt_to_rest()
            case "inventory":
                dungeon.state = GameState.INVENTORY_MANAGEMENT
                self._log("Select item")
                dungeon.push_event(InventoryManagementEvent(dungeon.player, mode="both"))
            case "spells":
                pass
            case "details":
                for item in dungeon.player.print_character_info():
                    self._log(item)
            case "describe":
                chamber = dungeon.player.current_chamber
                self._log(chamber.description)
            case _:
                raise GameActionError("Invalid Action")
                        
    def _call_for_combat_event(self, dungeon):
        if weighted_decision(0.5):
            character = enemy_factory()
            event = CombatEvent(character)
            self._log(f"You are attacked by an aggressive enemy")
            self._log(f"{character.name}")
            self._log(f"{character.description}")
            self._log("Choose your next action wisely")
            dungeon.push_event(event)

    def _call_for_contest(self, dungeon):
        contest_obj = trap_factory()
        self._log(f"You see a {contest_obj.name} trigger ahead of you")
        self._log(f"It is {contest_obj.description}")
        result = contest_obj.trigger_trap(dungeon.player)
        self._log(result)

    def _call_for_merchant_event(self, dungeon):
        dungeon.state = GameState.INVENTORY_MANAGEMENT
        merchant = merchant_factory()
        merchant_interaction = MerchantEvent(merchant)
        self._log(f"You meet a merchant named {merchant.name}")
        self._log("Select an item to purchase if you wish")
        dungeon.push_event(merchant_interaction)

    def _game_over_check(self, dungeon):
        if dungeon.player.character_death_check():
            self._log("You died")
            dungeon.event_stack = []
            dungeon.state = GameState.GAME_OVER
            print("You died")
