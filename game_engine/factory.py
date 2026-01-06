from .utilities.desc_utitlities import enemy_description
from .utilities.rng_utilities import random_integer
from .entities.characters.character import Character

def enemy_factory():
  enemy_info = enemy_description(2)
  name = enemy_info[0]
  desc = enemy_info[1]
  enemy = Character(name, desc)
  return enemy

def shop_factory():
  pass

def trap_factory():
  pass

