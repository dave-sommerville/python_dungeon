from ..events.event import Event
from ..game_action_error import GameActionError
class SkillContestEvent(Event):
    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return self.entity.options_list
    def resolve(self, dungeon, action):
        if action is self.entity.options_list[0]:
            if self.entity.skill_type is "dex":
                if dungeon.player.dex >= self.entity.skill_dc:
                    self.outcomes[0]
                else:
                    self.outcomes[1]
            if self.entity.skill_type is "con":
                if dungeon.player.con >= self.entity.skill_dc:
                    self.outcomes[0]
                else:
                    self.outcomes[1]
            if self.entity.skill_type is "wis":
                if dungeon.player.wis >= self.entity.skill_dc:
                    self.outcomes[0]
                else:
                    self.outcomes[1]
            if self.entity.skill_type is "cha":
                if dungeon.player.cha >= self.entity.skill_dc:
                    self.outcomes[0]
                else:
                    self.outcomes[1]
        elif action is self.entity.options_list[1]:
            self.outcomes[1]
        raise GameActionError("Invalid action")
