class InitializingEvent():
    def __init__(self):
        super().__init__(entity=None)
        self.creation_stage = 1
    def get_options(self):
        match self.creation_stage:
            case 1:
                return["Type your name"]
            case 2:
                return ["Enter a description of yourself, or enter x to skip"]
            case 3 | 4:
                return ["dex", "con", "wis", "cha"]
            # case _:
            #     raise GameActionError("Invalid action")

    def resolve(self, dungeon, action):
        match self.creation_stage:
            case 1:
                dungeon._msg("Please give us your name, player")
                dungeon.name_player(action)
                self.creation_stage += 1
                pass
            case 2:
                if action is "x":
                    self.creation_stage += 1
                else:
                    dungeon.describe_player(action)
                    self.creation_stage += 1
            case 3 | 4:
                self.creation_stage += 1
                dungeon._msg("You can select a skill to specialize in.")
            case _: 
                raise GameActionError("Out of range")
            