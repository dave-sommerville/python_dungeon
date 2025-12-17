from event import Event
class LevelUpEvent(Event):
    skill_points_assigned = 0
    def __init__(self, entity):
        super().__init__(entity)
    def get_options(self):
        return ["dex", "con", "wis", "cha"]

    def resolve(self, dungeon, action):
        if LevelUpEvent.skill_points_assigned < 2:
            print("You are levelling up. Your maxHP, modifier and skill points will all increase")
            dungeon.player.add_skill_point(action)
            LevelUpEvent.skill_points_assigned += 1
            if LevelUpEvent.skill_points_assigned >= 2:
                LevelUpEvent.skill_points_assigned = 0
                dungeon.player.maxHP += 10
                dungeon.player.modifer += 1
                dungeon.player.level += 1
                print(dungeon.player.maxHP)

                dungeon.current_event = None
