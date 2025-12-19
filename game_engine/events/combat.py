from .event import Event
from ..game_action_error import GameActionError
from ..game_states import GameState
from ..entities.characters.character import Character
class CombatEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "spell"]
    def resolve(self, dungeon, action):
        dungeon._msg(f"You are attacked by {self.entity.name}")
        dungeon._msg(f"They are {self.entity.description}")

        if isinstance(self.entity, Character) and dungeon.player.health > 0:
            dungeon._msg("Choose your next action wisely")
            match action:
                case "attack": # Sub events
                    dungeon.player.attack_action(self.entity)
                    if self.entity.character_death_check():
                        dungeon._msg("You killed the creature")
                        dungeon.current_event = None
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        dungeon._msg("The creature killed you")
                        dungeon.current_event = None
                        dungeon.state = GameState.GAME_OVER
                case "interact": # Sub events
                    dungeon._msg("You said hi and they left")
                    dungeon.current_event = None
                case "dodge":
                    dungeon._msg("You dodged")
                    dungeon.player.dodge_action()
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        dungeon._msg("The creature killed you")
                        dungeon.current_event = None

                case "retreat":
                    dungeon._msg("you retreat from the battle, but they get one attack")
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        dungeon._msg("The creature killed you")
                    dungeon.current_event = None
                case "spell": # Sub events
                    dungeon._msg("you cast a spell")
                    pass
                case _:
                    raise GameActionError("Invalid action")
        # Resolution for victory/defeat
