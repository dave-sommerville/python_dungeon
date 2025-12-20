from ..entities.entity import Entity
class ContestObject(Entity):
  def __init__(self, name, description, objective, skill_type, skill_dc, outcomes):
    super().__init__(name, description)
    # A door partially ajar, an acid spray, investigate history, search around, poison, lie, pick a lock

    self.objective_description = objective
    # Con, dex, wis, wis, con, cha, dex
    self.skill_type = skill_type
    self.skill_dc = skill_dc
    # (success, fail)
    self.outcomes = outcomes
  