from events.event import Event
from entities.characters.character import Character
class CombatEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "spell"]
    def resolve(self, dungeon, action):
        if isinstance(self.entity, Character) and dungeon.player.health > 0:
            print("Behold the might of Jeff")
            print(f"{self.entity.name} {self.entity.description}")
            match action:
                case "attack": # Sub events
                    dungeon.player.attack_action(self.entity)
                    if self.entity.character_death_check():
                        print("You killed the creature")
                        dungeon.current_event = None
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        print("The creature killed you")
                        dungeon.current_event = None
                case "interact": # Sub events
                    print("You said hi")
                case "dodge":
                    print("You dodged")
                    dungeon.player.dodge_action()
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        print("The creature killed you")
                        dungeon.current_event = None

                case "retreat":
                    print("you retreat from the battle, but they get one attack")
                    self.entity.attack_action(dungeon.player)
                    if dungeon.player.character_death_check():
                        print("The creature killed you")
                    dungeon.current_event = None
                case "spell": # Sub events
                    print("you cast a spell")
                    pass
                case _:
                    print("Invalid action")
        # Resolution for victory/defeat
