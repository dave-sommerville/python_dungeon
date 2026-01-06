from .utilities.desc_utitlities import enemy_description, weapon_description, base_item_description
from .utilities.rng_utilities import random_integer
from .entities.characters.character import Character
from .utilities.support_utilities import get_rarity
from .entities.items.item import Item
from .entities.items.weapon import Weapon
def enemy_factory():
  enemy_info = enemy_description(2)
  name = enemy_info[0]
  desc = enemy_info[1]
  enemy = Character(name, desc)
  return enemy

def item_factory(rarity):
  info_obj = base_item_description(rarity)
  name = info_obj[0]
  description = info_obj[1]
  durability = 1
  cost = random_integer((rarity+10), (rarity * 10))
  item = Item(name, description, durability, cost)
  return item

def weapon_factory(rarity):
  info_obj = weapon_description(rarity)
  name = info_obj[0]
  description = info_obj[1]
  damage = random_integer(rarity,(rarity * 10))
  attack_bonus = random_integer(rarity,(rarity * 10))
  weapon = Weapon(name, description, damage, attack_bonus)
  return weapon

def armor_factory():
  pass
def potion_factory():
  pass
def item_factory_generator():
  pass
def merchant_factory():
  merchant = Character("Jeff", "A small mushroom man.")
  shop_size = random_integer(2, 8)
  for i in range(shop_size):
    merchant.inventory.append(item_factory())
  return merchant
def trap_factory():
  pass

