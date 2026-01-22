from ..event import Event
from .combat_inventory import CombatInventoryEvent
from ...errors.game_action_error import GameActionError
from ...game_states import GameState
from ...entities.characters.character import Character
class CombatEvent(Event):

    def __init__(self, entity):
        super().__init__(entity)
    def enemy_death(self, dungeon):
        if self.entity.character_death_check():
            dungeon.pop_event()
            dungeon.state = GameState.MAIN_MENU
            dungeon.player.xp += self.entity.xp_award
            dungeon.player.killcount += 1
            return True
        else:
            return False

    def get_options(self):
        return ["attack", "interact", "dodge", "retreat", "use item"]
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
                    enemy_damage = self.entity.attack_action(dungeon.player)
                    if enemy_damage == 0:
                        dungeon._msg(f"{self.entity.name} attacks you but misses")
                    else:
                        dungeon._msg(f"{self.entity.name} attacks you and hits you for {enemy_damage} points of damage")
                case "interact": # Sub events
                    dungeon._msg("You said hi and they left")
                    dungeon.pop_event()
                    dungeon.state = GameState.MAIN_MENU
                case "dodge":
                    dungeon._msg("You dodged")
                    dungeon.player.dodge_action()
                    enemy_damage = self.entity.attack_action(dungeon.player)
                    if enemy_damage == 0:
                        dungeon._msg(f"{self.entity.name} attacks you but misses")
                    else:
                        dungeon._msg(f"{self.entity.name} attacks you and hits you for {enemy_damage} points of damage")
                case "retreat":
                    dungeon._msg("you retreat from the battle, but they get one attack")
                    enemy_damage = self.entity.attack_action(dungeon.player)
                    if enemy_damage == 0:
                        dungeon._msg(f"{self.entity.name} attacks you but misses")
                    else:
                        dungeon._msg(f"{self.entity.name} attacks you and hits you for {enemy_damage} points of damage")
                    dungeon.pop_event()
                    if dungeon.player.health > 0:
                        dungeon._msg("You retreat to a previous chamber")
                        direction = dungeon.player.get_possible_player_moves()
                        dungeon.move_player(direction)

                case "use item": # Sub events
                    dungeon._msg("Select an item to use")
                    dungeon.state = GameState.INVENTORY_MANAGEMENT
                    dungeon.push_event(CombatInventoryEvent(self.entity, dungeon.player))
                    pass
                case _:
                    raise GameActionError("Invalid action")
            
        # Resolution for victory/defeat
