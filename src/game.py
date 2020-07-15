import random
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator
from board import Board
from players.player import Player
from players.dumb_player import DumbPlayer
from players.random_player import RandomPlayer
from unit.unit import Unit
from unit.scout import Scout
from unit.destroyer import Destroyer
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.battleship import Battleship
from unit.dreadnaught import Dreadnaught
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.ship_yard import Ship_Yard
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy
from unit.carrier import Carrier


class Game:
    def __init__(self, grid_size):
        self.grid_size = grid_size  # ex [5,5]
        self.game_won = False
        self.players_dead = 0
        self.board = Board(grid_size)

    # main functions
    def initialize_game(self):
        self.board.players = self.create_players()
        self.board.create_planets_and_asteroids()

    def create_players(self):
        starting_positions = [[1, 1], [self.grid_size - 1, self.grid_size - 1],
                              [1, self.grid_size - 1], [self.grid_size - 1, 1]]
        colors = ['Blue', 'Red', 'Purple', 'Green']
        players = []
        for i in range(0, 4):
            type_of_player = random.randint(1, 2)  # dumb or random
            if type_of_player == 1:
                players.append(DumbPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))
            if type_of_player == 2:
                players.append(RandomPlayer(
                    starting_positions[i], self.grid_size, i + 1, colors[i]))

        return players

    def play(self):
        turn = 1
        self.player_has_not_won = True
        while self.player_has_not_won:
            self.player_has_not_won = self.check_if_player_has_won()
            print(self.player_has_not_won)
            if not self.player_has_not_won:
                break

            self.complete_turn(turn)

            turn += 1

        if self.players_dead >= (len(self.board.players) - 1):
            self.player_has_won()

    def player_has_won(self):
        self.state_obsolete()

        for player in self.board.players:
            if player.status == 'Playing':
                self.game_won = True
                print('Player', player.player_number, 'WINS!')

        exit()

    def check_if_player_has_won(self):
        for player in self.board.players:
            player.death_count = 0

            for ship in player.ships:
                if ship.status == 'Deceased':
                    player.death_count += 1
                    print(player.death_count)
                    player.ships.remove(ship)

            if player.death_count == len(player.ships):
                print(player, 'is dead')
                player.status = 'Deceased'

        self.players_dead = 0
        for player in self.board.players:
            if player.status == 'Deceased':
                self.players_dead += 1
            if self.players_dead == (len(self.board.players) - 1):
                return False
            else:
                return True

    def complete_turn(self, turn):
        print('--------------------------------------------------')
        print('Turn', turn)
        self.check_if_player_has_won()
        self.move_phase()
        self.combat_phase()
        self.economic_phase(turn)

    def move_phase(self):
        for player in self.board.players:
            player.check_colonization()
            for ship in player.ships:
                for _ in range(0, 3):  # 3 rounds of movements
                    ship.move()

        self.state_obsolete()

    def combat_phase(self):
        self.combat()

    def economic_phase(self, turn):
        for player in self.board.players:
            player.maintenance()
            player.creds += 20
            if turn % 2 == 0:
                player.upgrade()
            else:
                player.build_fleet(player.starting_position)

        print('Every Player got their daily allowence of', 20, 'creds.')

    # combat functions
    def combat(self):
        print('fighting (combat)')
        possible_fights_var = self.possible_fights()
        players_and_ships = []
        # print('num_of_possible_fights', num_of_possible_fights)
        for position in possible_fights_var:
            print(position)
            if len(position[0][2]
                   [1]) > 1:  # if 2 or more players are in current position

                # iterating through players and player's ships
                for player in position[0][2][2]:

                    players_and_ships.append([player, []])
                    print(players_and_ships)

                    for ship in player[
                            1]:  # iterating through the players ships
                        players_and_ships[position[0][2][2].index(
                            player)][1].append(ship)

                print('players and ships', players_and_ships)
                # ex. [[player1, [ship1, ship2]], [player2, [ship1]]]
                order = self.board.find_order_of_ships(players_and_ships)

                self.get_attackers_and_defenders_to_fight(order)

    def get_attackers_and_defenders_to_fight(self, order):

        for player in order:  # get attacking player
            random_attacking_ship = random.randint(0, len(player[1]))
            # get attacking ship
            attacking_ship = player[1][random_attacking_ship]
            attacking_player = player[0]

            while random.randint(0, len(order)) == order.index(player):
                random_for_defending_player = random.randint(
                    0, len(order))  # get defending player
                #
                defending_player = order[random_for_defending_player][0]

            random_for_defending_ship = random.randint(
                0, len(order[random_for_defending_player][1]))  # get defending
            # ship
            defending_ship = order[random_for_defending_player][1][
                random_for_defending_ship]

            self.ship_duel(attacking_player, defending_player, attacking_ship,
                           defending_ship)  # make 'em fight

    def ship_duel(self, player_1, player_2, ship_1, ship_2):
        print('FIGHT')
        if ship_1.status != 'Deceased' and ship_2.status != 'Deceased':

            if ship_1.fighting_class > ship_2.fighting_class:
                print("Player", player_1.player_number, "'s", ship_1.name,
                      ship_1.ID, "vs Player", player_2.player_number, "'s",
                      ship_2.name, ship_2.ID)
                self.hit_or_miss(player_1, player_2, ship_1, ship_2, 1)
            else:
                print("Player", player_1.player_number, "'s", ship_1.name,
                      ship_1.ID, "vs Player", player_2.player_number, "'s",
                      ship_2.name, ship_2.ID)
                self.hit_or_miss(player_1, player_2, ship_1, ship_2, 2)

            if ship_1.status == 'Deceased':
                print("Player", player_1.player_number,
                      "'s unit was destroyed at co-ords", [ship_1.x, ship_1.y])
                found_creds = random.randint(1, 10)
                player_1.creds -= found_creds
                player_2.creds += found_creds
                print('Player', player_2.player_number, 'found', found_creds,
                      'creds at co-ords', [ship_1.x, ship_1.y])
                print('-------------------------------------------')
                self.state_obsolete()

            elif ship_2.status == 'Deceased':
                print("Player", player_2.player_number,
                      "'s unit was destroyed at co-ords", [ship_2.x, ship_2.y])
                found_creds = random.randint(1, 10)
                player_1.creds += found_creds
                player_2.creds -= found_creds
                print('Player', player_1.player_number, 'found', found_creds,
                      'creds at co-ords', [ship_2.x, ship_2.y])
                print('-------------------------------------------')
                self.state_obsolete()

    def hit_or_miss(self, player_1, player_2, ship_1, ship_2, first_to_shoot):
        print('fighting (hit or miss)')
        while ship_1.armor > 0 and ship_2.armor > 0:  # if neither are dead
            if first_to_shoot == 1:  # player 1 shoots first
                hit_threshold = (ship_1.attack + player_1.attack_tech) - \
                    (ship_2.defense + player_2.defense_tech)
                die_roll = random.randint(1, 6)

                if die_roll == 1 or die_roll <= hit_threshold:
                    ship_2.armor -= 1  # player 2's ship loses some armor

                else:
                    print('Player', player_1.player_number,
                          'Missed their shot, targeting Player',
                          player_2.player_number, "'s unit", ship_2.name,
                          ship_2.ID)

            elif first_to_shoot == 2:  # player 2 shoots first
                hit_threshold = (ship_2.attack + player_2.attack_tech) - \
                    (ship_1.defense + player_1.defense_tech)
                die_roll = random.randint(1, 6)

                if die_roll == 1 or die_roll <= hit_threshold:
                    ship_1.armor -= 1  # player 1's ship loses some armor
                else:
                    print('Player', player_2.player_number,
                          'Missed their shot, targeting Player',
                          player_1.player_number, "'s unit", ship_1.name,
                          ship_1.ID)

        if ship_1.armor < 0:  #
            ship_1.status = 'Deceased'  # change statuses
        elif ship_2.armor < 0:  # of dead ships
            ship_2.status = 'Deceased'

    # misc functions
    def state_obsolete(self):  # obsolete but can be used for debugging
        for player in self.board.players:
            print('Player', player.player_number, ': Status:', player.status)
            print('')
            print('     Player Ships')
            for ship in player.ships:
                print('         ', ship.name, ':', 'Ship ID:',
                      ship.ID, ':', [ship.x, ship.y])

            print('')
            print('     Player Colonies')
            for colony in player.colonies:
                print('         ', colony.name, ':', 'Colony ID:',
                      colony.ID, ':', [colony.x, colony.y])

            print('     ')
            print('     Player Ship Yards')
            for ship_yard in player.ship_yards:
                print('         ', 'Ship Yard ID:', ship_yard.ID,
                      ':', [ship_yard.x, ship_yard.y])
            print('')
            print('')

    # helper functions

    def dice_roll(self, start, end):
        dice_1 = random.randint(start, end)
        dice_2 = random.randint(start, end - 1)
        if dice_1 > dice_2:
            return True
        elif dice_1 < dice_2:
            return False

    # helping combat function
    def possible_fights(self):
        positions_of_ships = []

        for i in range(0, self.grid_size + 1):
            for j in range(0, self.grid_size + 1):
                if len(
                        self.board.list_of_ships_at_x_y(
                            self.board.players, i, j)) > 0:
                    positions_of_ships.append(
                        self.board.list_of_ships_at_x_y(
                            self.board.players, i, j))  # ex below
        # tuples so no change #(((1,1), (3, ([player_1, (ship_1, ship_2)], [player_2, (ship_1)]))), ((2,3), (2, ([player_1, (ship_1, ship_2)])))
        print('positions_of_ships', positions_of_ships)
        return positions_of_ships