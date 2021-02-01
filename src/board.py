import random
from unit.colony_ship import Colony_Ship
from unit.colony import Colony
from unit.base import Base
from unit.miner import Miner
from unit.decoy import Decoy


class Board:
    # board_size is grid size and player_positions is the array of the home bases of players
    def __init__(self, game, board_size, asc_or_dsc):
        self.board_size = board_size
        self.game = game
        self.player_home_bases = [[self.board_size[0] // 2, 0], [self.board_size[0] // 2, self.board_size[1]], [0, self.board_size[1] // 2], [
            self.board_size[0], self.board_size[1] // 2]]
        self.ships_dict = {}
        self.misc_dict = {}
        self.dice_roll_index = 0
        if asc_or_dsc == 'asc':
            self.rolls = [1, 2, 3, 4, 5, 6]
        elif asc_or_dsc == 'dsc':
            self.rolls = [6, 5, 4, 3, 2, 1]
        self.planets = []
        self.asteroids = []
        #print('asc_or_dsc', asc_or_dsc)

    def update_board(self):
        for x in range(0, self.board_size[0] + 1):
            for y in range(0, self.board_size[1] + 1):
                ships_arr = []
                for player in self.game.players:
                    player_ships = player.ships + player.ship_yards + [player.home_base]
                    for ship in player_ships:
                        if ship.x == x and ship.y == y:
                            ships_arr.append(ship)
                if len(ships_arr) > 0:
                    self.ships_dict[(x, y)] = self.simple_sort(ships_arr)

    # create <instert thing here> stuffs
    def create_planets_and_asteroids(self):
        #print('create planets and asteroids')
        self.planets = []
        self.asteroids = []
        for x in range(0, self.board_size[0] + 1):
            for y in range(0, self.board_size[1] + 1):
                # 1,2 is a planet and 3,4, are asteroids and 5,6 are None
                if [x, y] != self.player_home_bases[0] and [x, y] != self.player_home_bases[1]:
                    planet_or_asteroid = 1  # self.get_die_roll()
                    if planet_or_asteroid <= 2:
                        self.misc_dict[(x, y)] = [self.create_planet([x, y])]
                        self.planets.append((x,y))
                        self.planets.append(self.create_planet([x, y]))
                    elif planet_or_asteroid > 2 and planet_or_asteroid <= 4:
                        self.misc_dict[(x, y)] = [self.create_asteroid([x, y])]
                        self.asteroids.append(self.create_asteroid([x, y]))

    def create_planet(self, position):
        return Planet(position, random.randint(0, 1))

    def create_asteroid(self, position):
        return Asteroid(position, random.randint(1, 2))

    def create_colony(self, player, planet, position):
        planet.is_colonized = True
        player.colonies.append(Colony(self, len(player.colonies) + 1, position, self.board_size))

    # combat stuffs
    def if_it_can_fight(self, ship): return not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy) and not isinstance(ship, Miner) and not isinstance(ship, Colony)

    def ship_1_fires_first(self, ship_1, ship_2):
        if ship_1.technology['tactics'] > ship_2.technology['tactics']:
            return True
        elif ship_1.technology['tactics'] < ship_2.technology['tactics']:
            return False
        else:
            if ship_1.technology['attack'] > ship_2.technology['attack']:
                return True
            elif ship_1.technology['attack'] < ship_2.technology['attack']:
                return False
            else:
                if ship_1.attack > ship_2.attack:
                    return True
                elif ship_1.attack < ship_2.attack:
                    return False
                else:
                    return True

    def get_die_roll(self):
        if self.dice_roll_index == 5:
            self.dice_roll_index = 0
        else:
            self.dice_roll_index += 1
        return self.rolls[self.dice_roll_index]

    def simple_sort(self, arr):
        fixed_arr, sorted_arr = [ship for ship in arr if ship.type != 'Colony' and ship.type != 'Colony Ship' and ship.type != 'Decoy' and ship.type != 'Miner'], []
        for ship in [ship for ship in arr if ship not in fixed_arr]:
            if ship.type == 'Colony':
                ship.player.colonies.remove(ship)
            else:
                ship.player.ships.remove(ship)
        while len(fixed_arr) > 0:
            strongest_ship = self.max_value(fixed_arr)
            sorted_arr.append(strongest_ship)
            fixed_arr.remove(strongest_ship)
        return sorted_arr

    def max_value(self, arr):     
        max_value = arr[0]
        if len(arr) > 1:
            for ship in arr[1:]:
                if ship.type == 'Home Base':
                    continue
                else:
                    if self.ship_1_fires_first(ship, max_value):
                        max_value = ship
        return max_value

class Planet:
    def __init__(self, position, tier, is_colonized = False):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.tier = tier  # habitiblity
        self.is_colonized = False
        self.ship_yards_at_planet = []
        self.is_claimed = False  # for colony ships finding nearest planet

class Asteroid:
    def __init__(self, position, tier):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.income = 5 * tier
