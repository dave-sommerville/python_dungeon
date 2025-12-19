from .character import Character
from ..items.potion import Potion
class Merchant(Character):
  def __init__(self, name, description):
    super().__init__(name, description)
    self.inventory = [Potion("Good Potion", "Fifty", 50), Potion("Bad Potion", "ten", 10)]
