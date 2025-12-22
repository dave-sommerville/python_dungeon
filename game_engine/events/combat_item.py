from .event import Event
class CombatItemEvent(Event):
    def __init__(self, entity, index, prev_event):
        super().__init__(entity)
        self.index = index
        self.prev_event = prev_event

    def get_options(self):
        return ["use", "back"]
    def resolve(self, dungeon, action):
        match action:
            case "use":
                self.entity.use_item(dungeon.player)
                dungeon.current_event = self.prev_event.prev_event
            case "back":
                dungeon.current_event = self.prev_event