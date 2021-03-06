import random
from unit.carrier import Carrier
from unit.decoy import Decoy
from unit.miner import Miner
from unit.base import Base
from unit.ship_yard import Ship_Yard
from unit.colony import Colony
from unit.colony_ship import Colony_Ship
from unit.dreadnaught import Dreadnaught
from unit.battleship import Battleship
from unit.battle_cruiser import BattleCruiser
from unit.cruiser import Cruiser
from unit.destroyer import Destroyer
from unit.scout import Scout
from unit.unit import Unit
from board import Planet
from board import Board
from player.player import Player
import sys
sys.path.append('src')


class CombatPlayer(Player):
    def __init__(self, position, board_size, player_index, player_color):
        super().__init__(position, board_size, player_index, player_color)
        self.type = 'Combat Player'
        self.creds = 0
        self.status = 'Playing'
        self.death_count = 0  # if winCount = amount of units self.lose = true
        # starts out with 3 scouts and 3 colony ships later it would be 3 miners
        self.ships = [
            Scout(self, 1, position, self.board_size, True),
            Scout(self, 2, position, self.board_size, True),
            Scout(self, 3, position, self.board_size, True),
            Colony_Ship(self, 4, position, self.board_size, True),
            Colony_Ship(self, 5, position, self.board_size, True),
            Colony_Ship(self, 6, position, self.board_size, True)
        ]
        self.ship_yards = [
            Ship_Yard(self, 1, position, self.board_size, False),
            Ship_Yard(self, 2, position, self.board_size, False),
            Ship_Yard(self, 3, position, self.board_size, False),
            Ship_Yard(self, 4, position, self.board_size, False)
        ]
        self.home_base = Colony(
            self, 1, position, self.board_size, home_base=True)
        self.colonies = []
        self.starting_position = position
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0
        self.terraform_tech = 0
        self.ship_size_tech = 0
        self.fighting_class_tech = 0
        self.movement_tech_upgrade_number = 0
        self.ship_to_build = 2

    def will_colonize_planet(self):
        return False

    def upgrade(self, turn):  # actual function should be in here because you can only upgrade new ships not ones in the field
        # print('upgrading')
        if turn == 1:
            if self.ship_size_tech < 6:  # biggest ship size that you can build
                self.ship_size_tech += 1
                self.creds -= 10
                print('Player', self.player_index, "upgraded their max building size from",
                      self.ship_size_tech - 1, 'to', self.ship_size_tech)
        else:
            while self.can_upgrade():
                stat_to_upgrade = random.randint(1, 6)
                #print('stat_to_upgrade', stat_to_upgrade)
                if stat_to_upgrade == 1 and self.attack_tech < 3:  # offense
                    self.attack_tech += 1
                    self.creds -= 10 * self.attack_tech
                    print('Player', self.player_index, 'upgraded their attack strength from',
                          self.attack_tech - 1, 'to', self.attack_tech)
                elif stat_to_upgrade == 2 and self.defense_tech < 3:  # defense
                    self.defense_tech += 1
                    self.creds -= 10 * self.defense_tech
                    print('Player', self.player_index, 'upgraded their defense strength from',
                          self.defense_tech - 1, 'to', self.defense_tech)
                elif stat_to_upgrade == 3 and self.fighting_class_tech < 3:  # tactics
                    self.fighting_class_tech += 1
                    self.creds -= 5 * self.fighting_class_tech + 10
                    print('Player', self.player_index, 'upgraded their fighting class from',
                          self.fighting_class_tech - 1, 'to', self.fighting_class_tech)
                elif stat_to_upgrade == 4 and self.movement_tech_upgrade_number < 5:  # speed
                    self.upgrade_movement_tech()
                elif stat_to_upgrade == 5 and self.ship_yard_tech < 2:  # ship yard
                    self.ship_yard_tech += 0.5
                    self.creds -= 10 * self.ship_yard_tech
                    print('Player', self.player_index, "upgraded their ship-yard's building size from",
                          self.ship_yard_tech - 1, 'to', self.ship_yard_tech)
                elif stat_to_upgrade == 6 and self.terraform_tech < 2:  # terraform
                    self.terraform_tech += 1
                    self.creds -= 15 * self.terraform_tech
                    print('Player', self.player_index, "upgraded their ablility to terraform from",
                          self.terraform_tech - 1, 'to', self.terraform_tech)
                else:
                    break

    def can_upgrade(self):
        return self.creds > 10 * self.attack_tech and self.creds > 10 * self.defense_tech and self.creds > 5 * self.fighting_class_tech + 10 and self.creds > 10 * self.movement_tech_upgrade_number + 10 and self.creds > 10 * self.ship_yard_tech and self.creds > 15 * self.terraform_tech

    def move(self, move_round):
        for ship in self.ships:
            # if not isinstance(ship, Base) and not isinstance(ship, Colony) and not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy):
            ship.move_to_center(move_round)
            # elif isinstance(ship, Colony_Ship):
            # ship.move_to_nearest_planet(self.board.misc_dict, Planet) # this is for laters

    def can_build_ships(self):
        if self.ship_to_build == 2 and self.creds >= 9 and self.ship_size_tech >= 1:
            return True
        elif self.ship_to_build == 1 and self.creds >= 6:
            return True
        else:
            return False

    def determine_availible_ship_classes(self):
        return self.ship_to_build

    def create_ship(self, ship_class, position):
        if ship_class == 1:
            return Scout(self, position, self.board_size, True)
        if ship_class == 2:
            return Destroyer(self, position, self.board_size, True)
