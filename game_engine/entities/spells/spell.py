from entity import Entity
from .spellbook import SpellBook
from .spellindex import SpellIndex

class Spell(Entity):
  def __init__(self, name, description, spell_index, mana_cost):
    super().__init__(name, description)
    self.spell_index = spell_index
    self.mana_cost = mana_cost
  
  def cast_spell(self):
    if self.spell_index == SpellIndex.STUN:
      pass
    if self.spell_index == SpellIndex.POISON:
      pass
    if self.spell_index == SpellIndex.HEAL:
      pass
    if self.spell_index == SpellIndex.FIREBALL:
      pass
    if self.spell_index == SpellIndex.LIFE_DRAIN:
      pass
    if self.spell_index == SpellIndex.SHIELD:
      pass
    else:
      pass # Needs an error
