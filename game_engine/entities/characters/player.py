from character import Character
# Extends Character

# Prisoner Status
# RestCount
# Positive Interaction
# IsPlaying
# Y, X, LocationID
# Weapon
# Armor
# XP
#Player Level
# Modifier
# Sanity
# Stats
# MaxHP
# Gold
# Mana
# Plot Levels
# NPC?
# Grey Crystal?
# Attack ranges
# Player Creation method

class Player(Character):
    some_other_property = ''
    def __init__(self, someProperty, someOtherProperty):
        super().__init__(someProperty)
        self.someOtherProperty = someOtherProperty
    def some_method(self):
        return "Override child class"