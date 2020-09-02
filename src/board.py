import random
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


class Board:
    # grid_size is grid size and player_positions is the array of the home bases of players
    def __init__(self, grid_size, asc_or_dsc):
        self.grid_size = grid_size
        self.players = []
        self.player_home_bases = [
            [self.grid_size // 2, 0], [self.grid_size // 2, self.grid_size]]
        self.ships_dict = {}
        self.misc_dict = {}
        self.dice_roll_index = 0
        if asc_or_dsc == 'asc':
            self.rolls = [1, 2, 3, 4, 5, 6]
        elif asc_or_dsc == 'dsc':
            self.rolls = [6, 5, 4, 3, 2, 1]

    # create <instert thing here> stuffs
    def create_planets_and_asteroids(self):
        #print('create planets and asteroids')
        self.planets = []
        self.asteroids = []
        for i in range(0, self.grid_size + 1):

            for j in range(0, self.grid_size + 1):
                # 1,2 is a planet and 3,4,5,6 are asteroids
                if not [i, j] == self.player_home_bases[0] or not [i, j] == self.player_home_bases[1]:
                    planet_or_asteroid = self.get_die_roll()

                    if planet_or_asteroid <= 2:
                        self.misc_dict[(i, j)] = self.create_planet([i, j])
                        self.planets.append(self.create_planet([i, j]))

                    elif planet_or_asteroid > 2:
                        self.misc_dict[(i, j)] = self.create_asteroid([i, j])
                        self.asteroids.append(self.create_asteroid([i, j]))

    def create_planet(self, position, tier = random.randint(0, 2)):
        return Planet(position, tier)

    def create_asteroid(self, position):
        size = random.randint(0, 2)
        tier = random.randint(0, 2)
        return Asteroid(position, size, tier)

    def create_colony(self, player, planet, position):
        planet.is_colonized = True
        player.colonies.append(Colony(self, len(player.colonies) + 1, position, self.grid_size))

    # combat stuffs
    def order_list_of_ships_at_x_y(self, x, y):
        ships_arr = []

        for player in self.players:  # array of ships

            for ship in player.ships:

                if ship.x == x and ship.y == y:

                    # if it can fight
                    if not isinstance(ship, Colony_Ship) and not isinstance(ship, Decoy) and not isinstance(ship, Miner) and not isinstance(ship, Colony):
                        #print('yes 1')
                        ships_arr.append(ship)

                    else:  # if not then die
                        player.ships.remove(ship)

        ordered_ships_arr = self.simple_sort(ships_arr)
        #print('ordered_ships_arr', ordered_ships_arr)
        self.ships_dict[(x, y)] = ordered_ships_arr


    def simple_sort(self, arr):  # merge sort
        newArr = []
        while len(arr) > 0:
            newArr.append(self.minimumValue(arr))
            arr.remove(self.minimumValue(arr))

        return newArr

    def minimumValue(self, arr):
        minimumVal = arr[0]

        if len(arr) >= 3:

            for i in range(1, len(arr)):

                if arr[i].fighting_class < minimumVal.fighting_class:

                    minimumVal = arr[i]

        elif len(arr) == 2:

            if arr[1].fighting_class < minimumVal.fighting_class:

                minimumVal = arr[1]

        return minimumVal

    def get_die_roll(self):
        if self.dice_roll_index == 5:
            self.dice_roll_index = 0
        else:
            self.dice_roll_index += 1

        return self.rolls[self.dice_roll_index]


class Planet:
    def __init__(self, position, tier):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.tier = tier  # habitiblity
        self.is_colonized = False
        self.ship_yards_at_planet = []


class Asteroid:
    def __init__(self, position, size, tier):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.tier = tier  # type of ore
        self.size = size  # scalar for tier
        # ex a tier 5 size 3 asteroird gives 15 creds while a tier 3 size 2 asteroid give 6 creds



