from ..characters.character import Character
class NPC(Character):
  def __init__(self, name, description):
    super().__init__(name, description)
    self.dialogue = []
    self.is_merchant = False
  