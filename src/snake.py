import numpy as np
from random import randrange
from sklearn.neighbors import DistanceMetric


class Snake:
    def __init__(self, weights=0, fitness=0):
        self.weights = weights
        self.fitness = fitness
        self.score = 0
        self.life_time = 0
        self.moves = 500

        self.direction = "right"
        self.food = [True, [0, 0]]
        self.s_x = 40
        self.s_y = 180
        self.body = [
            [self.s_x, self.s_y],
            [self.s_x - 10, self.s_y],
            [self.s_x - 20, self.s_y],
        ]

        self.died = False

        self.north_view = []
        self.south_view = []
        self.west_view = []
        self.east_view = []
        self.north_east_view = []
        self.south_east_view = []
        self.south_west_view = []
        self.north_west_view = []

        self.visualization()

    def place_food(self):
        if self.food[0]:
            self.food[1] = [randrange(2, 38) * 10, randrange(2, 38) * 10]
            self.food[0] = False

    def calc_fitness(self):
        self.fitness = self.score * 1000 + self.life_time

    def move(self):
        if self.direction == "down" and self.check(self.s_x, self.s_y + 10):
            self.s_y += 10
            self.body.insert(0, [self.s_x, self.s_y])
            self.visualization()

        elif self.direction == "up" and self.check(self.s_x, self.s_y - 10):
            self.s_y -= 10
            self.body.insert(0, [self.s_x, self.s_y])
            self.visualization()

        elif self.direction == "right" and self.check(self.s_x + 10, self.s_y):
            self.s_x += 10
            self.body.insert(0, [self.s_x, self.s_y])
            self.visualization()

        elif self.direction == "left" and self.check(self.s_x - 10, self.s_y):
            self.s_x -= 10
            self.body.insert(0, [self.s_x, self.s_y])
            self.visualization()

        self.moves -= 1
        self.life_time += 1

    def check(self, x, y):
        if x > 370 or y == 380 or x < 20 or y < 20:
            self.died = True
            return False

        if self.body[0] in self.body[1 : len(self.body)]:
            self.died = True
            return False

        if self.moves < 1:
            self.died = True
            return False

        if self.body[0] == self.food[1]:
            self.food[0] = True
            self.score += 1
            self.moves = 500
            return True

        self.body.pop()

        return True

    def brain(self, net):
        inputs = [0] * 28
        for i in range(8):
            inputs[i] = self.locate_food(i)
            inputs[i + 8] = self.locate_body(i)
            inputs[i + 16] = self.hit_wall(i)

        inputs[24] = 1 if self.direction == "up" else 0
        inputs[25] = 1 if self.direction == "down" else 0
        inputs[26] = 1 if self.direction == "left" else 0
        inputs[27] = 1 if self.direction == "right" else 0

        self.weights
        output = net.fitting(inputs, self.weights)
        output = np.argmax(output)

        if output == 0 and self.direction != "down":
            self.direction = "up"

        elif output == 1 and self.direction != "up":
            self.direction = "down"

        elif output == 2 and self.direction != "right":
            self.direction = "left"

        elif output == 3 and self.direction != "left":
            self.direction = "right"

    def visualization(self):
        # NORTH VISUALIZATION
        north_view_y = np.arange(self.body[0][1], 0, -10)
        north_view_x = np.full(north_view_y.shape, self.body[0][0], np.int)
        self.north_view = np.column_stack((north_view_x, north_view_y)).tolist()

        # SOUTH VISUALIZATION
        south_view_y = np.arange(self.body[0][1], 390, 10)
        south_view_x = np.full(south_view_y.shape, self.body[0][0], np.int)
        self.south_view = np.column_stack((south_view_x, south_view_y)).tolist()

        # WEST VISUALIZATION
        west_view_x = np.arange(self.body[0][0], 0, -10)
        west_view_y = np.full(west_view_x.shape, self.body[0][1], np.int)
        self.west_view = np.column_stack((west_view_x, west_view_y)).tolist()

        # EAST VISUALIZATION
        east_view_x = np.arange(self.body[0][0], 390, 10)
        east_view_y = np.full(east_view_x.shape, self.body[0][1], np.int)
        self.east_view = np.column_stack((east_view_x, east_view_y)).tolist()

        # NORTHEAST VISUALIZATION
        north_east_view_x = np.arange(self.body[0][0], 390, 10)
        north_east_view_y = np.arange(self.body[0][1], 0, -10)

        if north_east_view_x.shape[0] > north_east_view_y.shape[0]:
            self.north_east_view = np.column_stack(
                (north_east_view_x[: len(north_east_view_y)], north_east_view_y)
            ).tolist()

        else:
            self.north_east_view = np.column_stack(
                (north_east_view_x, north_east_view_y[: len(north_east_view_x)])
            ).tolist()

        # SOUTHEAST VISUALIZATION
        south_east_view_x = np.arange(self.body[0][0], 390, 10)
        south_east_view_y = np.arange(self.body[0][1], 390, 10)

        if south_east_view_x.shape[0] > south_east_view_y.shape[0]:
            self.south_east_view = np.column_stack(
                (south_east_view_x[: len(south_east_view_y)], south_east_view_y)
            ).tolist()

        else:
            self.south_east_view = np.column_stack(
                (south_east_view_x, south_east_view_y[: len(south_east_view_x)])
            ).tolist()

        # SOUTHWEST VISUALIZATION
        south_west_view_x = np.arange(self.body[0][0], 0, -10)
        south_west_view_y = np.arange(self.body[0][1], 390, 10)

        if south_west_view_x.shape[0] > south_west_view_y.shape[0]:
            self.south_west_view = np.column_stack(
                (south_west_view_x[: len(south_west_view_y)], south_west_view_y)
            ).tolist()

        else:
            self.south_west_view = np.column_stack(
                (south_west_view_x, south_west_view_y[: len(south_west_view_x)])
            ).tolist()

        # NORTHWEST VISUALIZATION
        north_west_view_x = np.arange(self.body[0][0], 0, -10)
        north_west_view_y = np.arange(self.body[0][1], 0, -10)

        if north_west_view_x.shape[0] > north_west_view_y.shape[0]:
            self.north_west_view = np.column_stack(
                (north_west_view_x[: len(north_west_view_y)], north_west_view_y)
            ).tolist()

        else:
            self.north_west_view = np.column_stack(
                (north_west_view_x, north_west_view_y[: len(north_west_view_x)])
            ).tolist()

    def locate_food(self, view):
        if view == 0:
            if self.food[1] in self.north_view:
                return 1

            else:
                return 0

        elif view == 1:
            if self.food[1] in self.south_view[1:]:
                return 1

            else:
                return 0

        elif view == 2:
            if self.food[1] in self.west_view[1:]:
                return 1

            else:
                return 0

        elif view == 3:
            if self.food[1] in self.east_view[1:]:
                return 1

            else:
                return 0

        elif view == 4:
            if self.food[1] in self.north_east_view[1:]:
                return 1

            else:
                return 0

        elif view == 5:
            if self.food[1] in self.south_east_view[1:]:
                return 1

            else:
                return 0

        elif view == 6:
            if self.food[1] in self.south_west_view[1:]:
                return 1

            else:
                return 0

        elif view == 7:
            if self.food[1] in self.north_west_view[1:]:
                return 1

            else:
                return 0

    def locate_body(self, view):
        if view == 0:
            if self.direction == "down":
                return 0

            for cord in self.north_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 11:
                        return 1
                    else:
                        return 0

            return 0

        elif view == 1:
            if self.direction != "up":
                return 0

            for cord in self.south_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 11:
                        return 1
                    else:
                        return 0

            return 0

        elif view == 2:
            if self.direction == "right":
                return 0

            for cord in self.west_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 11:
                        return 1
                    else:
                        return 0

            return 0

        elif view == 3:
            if self.direction == "left":
                return 0

            for cord in self.east_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 11:
                        return 1
                    else:
                        return 0
            return 0

        elif view == 4:
            for cord in self.north_east_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 21:
                        return 1
                    else:
                        return 0
            return 0

        elif view == 5:
            for cord in self.south_east_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 21:
                        return 1
                    else:
                        return 0
            return 0

        elif view == 6:
            for cord in self.south_west_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 21:
                        return 1
                    else:
                        return 0
            return 0

        elif view == 7:
            for cord in self.north_west_view[1:]:
                if cord in self.body[1:]:
                    if self.manhattan(self.body[0], cord) < 21:
                        return 1
                    else:
                        return 0

            return 0

    def hit_wall(self, view):
        if view == 0:
            if self.manhattan(self.body[0], self.north_view[-1]) < 11:
                return 1

            else:
                return 0

        elif view == 1:
            if self.manhattan(self.body[0], self.south_view[-1]) < 11:
                return 1

            else:
                return 0

        elif view == 2:
            if self.manhattan(self.body[0], self.west_view[-1]) < 11:
                return 1

            else:
                return 0

        elif view == 3:
            if self.manhattan(self.body[0], self.east_view[-1]) < 11:
                return 1

            else:
                return 0

        elif view == 4:
            if self.manhattan(self.body[0], self.north_east_view[-1]) < 21:
                return 1

            else:
                return 0

        elif view == 5:
            if self.manhattan(self.body[0], self.south_east_view[-1]) < 21:
                return 1

            else:
                return 0

        elif view == 6:
            if self.manhattan(self.body[0], self.south_west_view[-1]) < 21:
                return 1

            else:
                return 0

        elif view == 7:
            if self.manhattan(self.body[0], self.north_west_view[-1]) < 21:
                return 1

            else:
                return 0

    def manhattan(self, coord_A, coord_B):
        dist = DistanceMetric.get_metric("manhattan")
        result = dist.pairwise([coord_A, coord_B])
        return result[0][1]

    def __lt__(self, other):
        return self.fitness > other.fitness