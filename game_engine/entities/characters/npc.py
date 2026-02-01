from ..characters.character import Character
class NPC(Character):
  def __init__(self, name, description, response_one, response_two):
    super().__init__(name, description)
    self.dialogue_options = []
    self.response_one = response_one
    self.response_two = response_two