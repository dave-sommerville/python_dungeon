from ..entities.entity import Entity
from ..game_action_error import GameActionError
from ..utilities.rng_utilities import random_integer
class ContestObject(Entity):
  def __init__(self, name, description, skill_type, skill_dc):
    super().__init__(name, description)
    # wis, con, cha, dex
    self.skill_type = skill_type
    self.skill_dc = skill_dc
    self.damage_range = (10,40)
    # (success, fail) outcomes
    self.outcomes = ("You are caught in the trap","You successfully avoid damage.")
  def trigger_trap(self, character):
    player_stat = getattr(character, self.skill_type, None)
    if player_stat is None:
      raise GameActionError("Invalid skill type")
    if player_stat >= self.skill_dc:
        damage = random_integer(self.damage_range[0], self.damage_range[1])
        character.health -= damage
        return f"{self.outcomes[0]}. You take {damage} points of damage"
    else:
        return self.outcomes[1]
