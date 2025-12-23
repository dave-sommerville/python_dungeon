from .event import Event
from .combat_inventory import CombatInventoryEvent
from ..game_action_error import GameActionError
from ..game_states import GameState
from ..entities.characters.character import Character
class CombatEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
    def enemy_death(self, dungeon):
        if self.entity.character_death_check():
            dungeon._msg("You killed the creature")
            dungeon.current_event = None
            dungeon.state = GameState.MAIN_MENU
            dungeon.player.xp += self.entity.xp_award
            dungeon.player.killcount += 1
            return True
        else:
            return False

    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "use item"]
    def resolve(self, dungeon, action):
        dungeon._msg(f"You are attacked by {self.entity.name}")
        dungeon._msg(f"They are {self.entity.description}")

        if isinstance(self.entity, Character) and dungeon.player.health > 0:
            dungeon._msg("Choose your next action wisely")
            match action:
                case "attack": # Sub events
                    dungeon.player.attack_action(self.entity)
                    if self.enemy_death(dungeon):
                        return
                    self.entity.attack_action(dungeon.player)
                case "interact": # Sub events
                    dungeon._msg("You said hi and they left")
                    dungeon.current_event = None
                    dungeon.state = GameState.MAIN_MENU

                case "dodge":
                    dungeon._msg("You dodged")
                    dungeon.player.dodge_action()
                    self.entity.attack_action(dungeon.player)

                case "retreat":
                    dungeon._msg("you retreat from the battle, but they get one attack")
                    self.entity.attack_action(dungeon.player)
                    dungeon.current_event = None
                    dungeon.state = GameState.MAIN_MENU

                case "use item": # Sub events
                    dungeon._msg("Select an item to use")
                    dungeon.state = GameState.INVENTORY_MANAGEMENT
                    dungeon.current_event = CombatInventoryEvent(self.entity, self, dungeon.player)
                    pass
                case _:
                    raise GameActionError("Invalid action")
            
        # Resolution for victory/defeat
