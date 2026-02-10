from .event import Event
from .inventory_management import InventoryManagementEvent
from .spell_management import SpellManagementEvent
from ..errors.game_action_error import GameActionError
from ..entities.characters.character import Character

class CombatEvent(Event):
    def __init__(self, entity):
        super().__init__(entity)
    def enemy_death(self, dungeon):
        if self.entity.character_death_check():
            dungeon.pop_event()
            dungeon.player.xp += self.entity.xp
            dungeon.player.killcount += 1
            return True
        else:
            return False

    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "use item", "cast spell"]
    
    def resolve(self, dungeon, action):
        if isinstance(self.entity, Character) and dungeon.player.health > 0:
            match action:
                case "attack": # Sub events
                    player_damage = dungeon.player.attack_action(self.entity)
                    if player_damage == 0:
                        dungeon._msg("You attempt to strike, but miss your foe")
                    else:
                        dungeon._msg(f"You attack and strike your foe for {player_damage} points of damage")
                    if self.enemy_death(dungeon):
                        dungeon._msg("Your attack is enough to vanquish your enemy")
                        return
                    self._enemy_attack(dungeon)
                case "interact": # Sub events
                    dungeon._msg("You said hi and they left")
                    dungeon.pop_event()
                case "dodge":
                    dungeon._msg("You dodged")
                    dungeon.player.dodge_action()
                    self._enemy_attack(dungeon)
                case "retreat":
                    dungeon._msg("you retreat from the battle, but they get one attack")
                    enemy_damage = self.entity.attack_action(dungeon.player)
                    self._enemy_attack(dungeon)
                    if dungeon.player.health > 0:
                        direction = dungeon.player.get_possible_player_moves()
                        dungeon._msg(f"You retreat {direction} to a previous chamber")
                        dungeon.move_player(direction)
                case "cast spell":
                    dungeon._msg("Select a spell to case")
                    dungeon.push_event(SpellManagementEvent(dungeon.player, self.entity))
                case "use item": # Sub events
                    dungeon._msg("Select an item to use")
                    dungeon.push_event(InventoryManagementEvent(dungeon.player, mode="use"))
                    self._enemy_attack(dungeon)
                case _:
                    raise GameActionError("Invalid action")
                
    def _enemy_attack(self, dungeon):
        enemy_damage = self.entity.attack_action(dungeon.player)
        if enemy_damage == 0:
            dungeon._msg(f"{self.entity.name} attacks you but misses")
        else:
            dungeon._msg(f"{self.entity.name} attacks you and hits you for {enemy_damage} points of damage")

        # Resolution for victory/defeat
