from entities.characters.monster import Monster
class CombatEvent:
    event_id = 0
    enemies = Monster()

    def __init__(self, event_id, enemies):
        self.event_id = event_id
        self.enemies = enemies
    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "spell"]
    def _resolve(self, player, action):
        while self.enemies and player.health > 0:
            match action:
                case "attack": # Sub events
                    pass
                case "interact": # Sub events
                    pass
                case "dodge":
                    pass
                case "retreat":
                    pass
                case "spell": # Sub events
                    pass
                case _:
                    print("Invalid action")
        # Resolution for victory/defeat
