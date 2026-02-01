from .utilities.desc_utitlities import enemy_description, weapon_description, base_item_description, armor_description, potion_description, trap_description
from .utilities.rng_utilities import random_integer
from .entities.characters.character import Character
from .entities.items.item import Item
from .entities.items.weapon import Weapon
from .entities.items.armor import Armor
from .entities.items.potion import Potion
from .entities.contest_object import ContestObject
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
  item = Item(name, description)
  item.durability = 1
  item.cost = random_integer(rarity, (rarity * 5))
  return item

def weapon_factory(rarity):
  info_obj = weapon_description(rarity)
  name = info_obj[0]
  description = info_obj[1]
  damage = random_integer(rarity,(rarity * 10))
  attack_bonus = random_integer(rarity,(rarity * 10))
  weapon = Weapon(name, description, damage, attack_bonus)
  return weapon

def armor_factory(rarity):
  info_obj = armor_description(rarity)
  name = info_obj[0]
  description = info_obj[1]
  ac_bonus = random_integer(rarity,(rarity * 2))
  armor = Armor(name, description, ac_bonus)
  return armor

def potion_factory(rarity):
  info_obj = potion_description()
  name = info_obj[0]
  description = info_obj[1]
  potion = Potion(name, description)
  potion.potency = rarity
  return potion

def random_item_factory(rarity):
  choice = random_integer(1,100)
  if choice > 80:
    return item_factory(rarity)
  elif choice > 60:
    return weapon_factory(rarity)
  elif choice > 30:
    return armor_factory(rarity)
  else:
    return potion_factory(rarity)
# Add cost randomizer based on CHA
def merchant_factory():
  merchant = Character("Jeff", "A small mushroom man.")
  shop_size = random_integer(1, 4)
  for i in range(shop_size):
    rarity = random_integer(1,10)
    item = random_item_factory(rarity)
    merchant.inventory.append(item)
  return merchant
def trap_factory():
  info_obj = trap_description()
  name = info_obj[0]
  desc = info_obj[1]
  skill_type = info_obj[2]
  skill_dc = random_integer(1,5)
  trap = ContestObject(name, desc, skill_type, skill_dc)
  return trap

