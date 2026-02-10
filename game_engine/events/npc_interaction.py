from .event import Event
from ..errors.game_action_error import GameActionError

class NpcInteractionEvent(Event):
    def __init__(self, entity, enemy, dialogue_options):
        super().__init__(entity)
        self.enemy = enemy
        self.stage = 0
        self.selected_index = None
        self.dialogue_options = dialogue_options

    def get_options(self):
        """Return options based on current stage."""
        return self.entity.dialogue_options
        
    def resolve(self, dungeon, action):
        """Process user action based on current stage."""
        if action == "ignore":
            # Pop this event and return to previous
            dungeon.pop_event()
            return
        if action == self.entity.dialogue_options[0]:
            dungeon._msg(f"{self.entity.name} replies:")
            dungeon._msg(self.entity.response_one)
            del self.entity.dialogue_options[0]
        elif action == self.entity.dialogue_options[1]:
            dungeon._msg(f"{self.entity.name} replies:")
            dungeon._msg(self.entity.response_two)
            del self.entity.dialogue_options[1]
        else:
            raise GameActionError("Invalid Action")
