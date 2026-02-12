from ..characters.character import Character
from ...utilities.rng_utilities import weighted_decision, random_integer

class NPC(Character):
  def __init__(self, name, description, dialogue_options, response_one, response_two):
    super().__init__(name, description)
    self.dialogue_options = dialogue_options
    self.response_one = response_one
    self.response_two = response_two

