from .game_states import GameState
from .game_action_error import GameActionError
from .locations.dungeon import Dungeon
from .entities.characters.character import Character
from .events.combat import CombatEvent
from .events.skill_contest import SkillContestEvent
from .events.merchant_interaction import MerchantEvent
from .events.inventory_item import InventoryItemEvent
from .utilities.rng_utilities import weighted_decision
from .entities.contest_object import ContestObject
from .entities.characters.npc import NPC
from .entities.items.item import Item
from .entities.items.armor import Armor

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
            dungeon.message_buffer.extend(self.logs)
            self.logs = dungeon.message_buffer
            dungeon.message_buffer = []
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

    def _call_for_combat_event(self, dungeon):
        if weighted_decision(0.5):
            character = Character("Jeff", "The Skeleton")
            event = CombatEvent(character)
            self._log(f"You are attacked by an aggressive enemy")
            self._log(f"{character.name}")
            self._log(f"{character.description}")
            self._log("Choose your next action wisely")
            dungeon.current_event = event

    def _take_damage(self):
        self._log("You take damage")
        pass
    def _take_half_damage(self):
        self._log("You take half damage")

    def _call_for_contest_event(self, dungeon):
        dungeon.state = GameState.INVENTORY_MANAGEMENT
        contest_obj = ContestObject("Acid spray", "", "", ["Jump away", "Ignore"], "dex", 15, [self._take_damage, self._take_half_damage])
        contest = SkillContestEvent(contest_obj)
        self._log(f"You see a trap. What do you do?")
        dungeon.current_event = contest

    def _call_for_merchant_event(self, dungeon):
        dungeon.state = GameState.INVENTORY_MANAGEMENT
        merchant = NPC("Also jeff", "idk, a little mushroom guy")
        merchant.is_merchant = True
        merchant.inventory = [Item("For Sale","Urn"), Item("For sale","Jug")]
        merchant_interaction = MerchantEvent(merchant)
        self._log(f"You meet a merchant")
        dungeon.current_event = merchant_interaction
    # Has to check the room's direction for sneaky players
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
                self._call_for_contest_event(dungeon)
            case "search":
                loot_list = dungeon.player.search_chamber()
                for item in loot_list:
                    dungeon._msg(item)
            case "rest":
                dungeon.attempt_to_rest()
            case "inventory":
                dungeon.state = GameState.INVENTORY_MANAGEMENT
                self._log("Select item")
                pass
            case "spells":
                pass
            case "details":
                for item in dungeon.player.print_player_info():
                    self._log(item)
            case "describe":
                chamber = dungeon.player.current_chamber
                self._log(chamber.description)
            case _:
                raise GameActionError("Invalid Action")

    def _resolve_inventory_management_menu(self, dungeon, action):
        player = dungeon.player
        if action == "back":
            dungeon.state = GameState.MAIN_MENU
            return
        # Accept a plain digit (sent from the UI as the index), or a leading-index form like "0: Sword"
        if isinstance(action, str) and action.isdigit():
            index = int(action)
            if 0 <= index < len(player.inventory):
                item = player.inventory[index]
                self._log(item.item_description())
                dungeon.current_event = InventoryItemEvent(item, index)
                return
        # Backwards-compatible: parse "0: Name" style
        if isinstance(action, str) and ":" in action:
            index_part = action.split(":")[0].strip()
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
                return dungeon.player.print_character_inventory()
            case GameState.SPELL_MANAGEMENT:
                return ["cast", "inspect", "back"]
            case _:
                raise GameActionError("Invalid Action")