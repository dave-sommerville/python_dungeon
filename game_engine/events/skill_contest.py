from ..events.event import Event
from ..game_action_error import GameActionError
from ..game_states import GameState

class SkillContestEvent(Event):
    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return self.entity.options_list
    def resolve(self, dungeon, action):
        print(type(action))
        print(self.entity.options_list[0])
        index = int(action)
        if index == 0:
            player_stat = getattr(dungeon.player, self.entity.skill_type, None)
            if player_stat is None:
                raise GameActionError("Invalid skill type")
            if player_stat >= self.entity.skill_dc:
                self.entity.outcomes[0]()
            else:
                self.entity.outcomes[1]()
            dungeon.state = GameState.MAIN_MENU
            dungeon.current_event = None
            return
        elif index == 1:
            self.entity.outcomes[1]()
            dungeon.state = GameState.MAIN_MENU
            dungeon.current_event = None
            return
        raise GameActionError("Invalid action")
