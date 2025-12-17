from events.event import Event
from entities.characters.character import Character
class CombatEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "spell"]
    def _resolve(self, dungeon, action):
        if isinstance(self.entity, Character) and dungeon.player.health > 0:
            print("Behold the might of Jeff")
            print(f"{self.entity.name}{self.entity.description}")
            match action:
                case "attack": # Sub events
                    self.entity.health -= 10
                    print(self.entity.health)
                    pass
                case "interact": # Sub events
                    print("You said hi")
                case "dodge":
                    print("You dodged")
                case "retreat":
                    print("you retreat from the battle")
                    dungeon.current_event = None
                case "spell": # Sub events
                    print("you cast a spell")
                    pass
                case _:
                    print("Invalid action")
        # Resolution for victory/defeat
