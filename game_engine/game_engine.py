from game_states import GameState
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
        event.resolve(action, dungeon)


    def _resolve_state_action(self, dungeon, action):
        match dungeon.state:
            case GameState.MAIN_MENU:
                self._resolve_main_menu(dungeon, action)
            case GameState.COMBAT:
                self._resolve_main_menu(dungeon, action)
            case _:
                print("Invalid State")
