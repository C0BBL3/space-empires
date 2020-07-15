import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Unit:
    def __init__(self, ID, position, grid_size, can_move=True, attack_tech=0, defense_tech=0, movement_tech=0, ship_yard_tech=0):
        self.ID = ID
        self.x = position[0]
        self.y = position[1]
        self.grid_size = grid_size
        self.status = 'Playing'  # for ship yard and other stuffs
        self.can_move = can_move
        self.attack_tech = 0
        self.defense_tech = 0
        self.movement_tech = [1, 1, 1]
        self.ship_yard_tech = 0

    def move(self, dumb_player = False):
        # print('moving')
        # 0 is up   1 is right    2 is down   3 is left
        direction = random.randint(0, 3)
        if self.can_move and not dumb_player:
            # print(direction)
            for i in range(0, len(self.movement_tech)):
                for _ in range(0, self.movement_tech[i]):
                    if direction == UP:
                        if self.y > 0:
                            self.y -= 1
                        elif self.y <= 0:
                            self.y += 1
                    elif direction == DOWN:
                        if self.y < self.grid_size:
                            self.y += 1
                        elif self.y >= self.grid_size:
                            self.y -= 1
                    elif direction == RIGHT:
                        if self.x < self.grid_size:
                            self.x += 1
                        elif self.x >= self.grid_size:
                            self.x -= 1
                    elif direction == LEFT:
                        if self.x > 0:
                            self.x -= 1
                        elif self.x <= 0:
                            self.x += 1

        if self.can_move and dumb_player: #so dumb player only moves right
            for i in range(0, len(self.movement_tech)):
                for _ in range(0, self.movement_tech[i]):
                    if self.x < self.grid_size:
                        self.x += 1