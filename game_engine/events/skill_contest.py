from ..events.event import Event
class SkillContestEvent(Event):
    def __init__(self, entity):
        super().__init__(entity)
    def get_options():
        return [""]
    def resolve(self, dungeon, action):
        pass