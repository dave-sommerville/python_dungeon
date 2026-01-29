from ...entities.entity import Entity
class Spell(Entity):
  def __init__(self, name, description, spell_effect, mana_cost, potency):
    super().__init__(name, description)
    self.spell_effect = spell_effect
    self.mana_cost = mana_cost
    self.potency = potency
  
  def cast_spell(self, player, target):
    if player.mana >= self.mana_cost:
      self.spell_effect(player,target, self.potency)
      player.mana -= self.mana_cost
      return "Spell cast successfully."
    else:
      return "You don't have enough mana to cast that spell."
    
