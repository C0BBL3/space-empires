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
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.players = []
        self.player_home_bases = [
            [1, 1], [self.grid_size - 1, self.grid_size - 1]]

        for position in self.player_home_bases:
            self.create_planet(position)

    # check stuffs
    def check_colonization(self):
        print('check colonization')
        for player in self.players:

            for ship in player.ships:

                if isinstance(ship, Colony_Ship):

                    for planet in self.planets:

                        if ship.x == planet.x and ship.y == planet.y and not planet.is_colonized:
                            print('it do be colonized')
                            if ship.terraform_tech >= 4 - planet.tier:  # if the colony ship can colonize the planet
                                print('Player', player.player_number,
                                      'just colonized a tier', planet.tier,
                                      'planet at co-ords:',
                                      (planet.x, planet.y))
                                self.create_colony(
                                    player, planet, planet.position)
                                index = player.ships.index(ship)
                                player.ships.remove(player.ships[index])

                            else:
                                print('Player', player.player_number,
                                      "can't colonize a tier", planet.tier,
                                      'planet at co-ords:',
                                      (planet.x, planet.y),
                                      'because their terraform tech is',
                                      ship.terraform_tech)

    # create <instert thing here> stuffs
    def create_planets_and_asteroids(self):
        print('create planets and asteroids')
        self.planets = []
        self.asteroids = []
        for player_position in self.player_home_bases:  # create home base
            self.create_planet(player_position)

        for i in range(0, self.grid_size + 1):

            for j in range(0, self.grid_size + 1):
                # 1,2 is a planet and 3,4,5,6,7,8 are asteroids
                planet_or_asteroid = random.randint(1, 8)

                if planet_or_asteroid <= 2:
                    self.planets.append(self.create_planet([i, j]))

                elif planet_or_asteroid > 2:
                    self.asteroids.append(self.create_asteroid([i, j]))

    def create_planet(self, position):
        tier = random.randint(1, 3)
        return Planet(position, tier)

    def create_asteroid(self, position):
        size = random.randint(1, 3)
        tier = random.randint(1, 5)
        return Asteroid(position, size, tier)

    def create_colony(self, player, planet, position):
        planet.is_colonized = True
        player.colonies.append(
            Colony(len(player.colonies) + 1, position, self.grid_size))

    # combat stuffs
    # [[player1, [ship1, ship2]], [player2, [ship1]]]

    def find_order_of_ships(self, player_ships):
        print('fighting (find order)')
        order = []

        for player_1 in player_ships:  # array of ships

            for player_2 in player_ships:  # array of ships

                #print('player1', player_1)
                #print('player2', player_2)

                for ship_1 in player_1.ships:  # ship

                    for ship_2 in player_2.ships:  # ship

                        if ship_1.fighting_class > ship_2.fighting_class:
                            order.append((player_ships.index(player_1),
                                          ship_1))

                        elif ship_2.fighting_class > ship_1.fighting_class:
                            order.append((player_ships.index(player_2),
                                          ship_2))

                        else:

                            if ship_1.attack > ship_2.attack:
                                order.append((player_ships.index(player_1),
                                              ship_1))

                            elif ship_2.attack > ship_1.attack:
                                order.append((player_ships.index(player_2),
                                              ship_2))
        print('order', order)
        return order

    def list_of_ships_at_x_y(self, players, x, y):
        count = 0
        all_data = []
        temp = []
        player_and_ships_arr = []

        for player in players:  # array of ships
            player_counted = False
            count = 0
            player_and_ships_arr = []

            for ship in player.ships:

                if ship.x == x and ship.y == y and not player_counted:
                    count += 1
                    player_counted = True

            #print('count', count)

            if count > 1:  # if more than 1 ship in current position
                player_and_ships_arr.append(player)
                player_and_ships_arr.append([])
                #print('player and ships', player_and_ships_arr)

                for ship in player.ships:  # ship

                    if ship.x == x and ship.y == y:

                        if ship.name != Colony_Ship or ship.name != Decoy or ship.name != Miner:  # if it can fight
                            player_and_ships_arr[1].append(ship)

                        else:  # if not then die
                            player.ships.remove(ship)

            # print('player and ships', player_and_ships_arr) #player and ships

            # if len(player_and_ships_arr) > 0:
            # print('player', player_and_ships_arr[0]) #player
            # print('ships', player_and_ships_arr[1]) #arr of ships

            if len(player_and_ships_arr) > 0:
                temp.append((x, y))
                temp.append(count)
                temp.append(player_and_ships_arr)
                all_data.append(temp)

            all_data = self.screen_ship_combat(player_and_ships_arr)

        #print('all_data', all_data)
        # ((0,0), (3, ([player_1, (ship_1, ship_2)], [player_2, (ship_1)])), (1,0), (3, ([player_1, (ship_1)], [player_2, (ship_1, ship_2)]
        return all_data

    def screen_ship_combat(self, data):
        for position in data:
            players = []

            for player in position[1][1]:
                players.append(players)

            for player_1 in player:

                for player_2 in player:

                    if player_1 != player_2:

                        if len(player_1.ships) > len(player_2.ships):

                            for i in range(len(player_1.ships), len(player_2.ships), -1):
                                player_1.ships.pop()

                        elif len(player_1.ships) < len(player_2.ships):

                            for i in range(len(player_2.ships), len(player_1.ships), -1):
                                player_2.ships.pop()

        return data


class Planet:
    def __init__(
            self, position, tier
    ):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        # self.size = size #max number of ship yards
        self.tier = tier  # habitiblity
        self.is_colonized = False
        self.ship_yards_at_planet = []


class Asteroid:
    def __init__(
            self, position, size, tier
    ):  # tier 1 uninhabitable at all like a small moon, tier 2 is barren, like mars, but only habitable by terraform 2 colony ships tier 3 is like earth, fully habatible by any colony ship
        self.position = position
        self.x = position[0]
        self.y = position[1]
        # self.size = size #max number of ship yards
        self.tier = random.randint(0, 5)  # type of ore
        self.size = size  # scalar for tier
        # ex a tier 5 size 3 asteroird gives 15 creds while a tier 3 size 2 asteroid give 6 creds