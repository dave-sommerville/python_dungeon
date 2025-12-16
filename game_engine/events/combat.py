class CombatEvent:
    def _resolve_combat_menu(self, player, action):
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
