import os
import numpy as np
from typing import List
from .net import NeuralNet
from .ge import Genetic
from .snake import Snake


class Population:
    def __init__(self, size, inp, hid, out):
        self.size = size
        self.records = [
            0,
            0,
            0,
            0,
        ]  # [Best Generations, Best Score, Best Life Time, Best Fitness]
        self.generation = 1
        self.plot = []
        self.ge = Genetic()
        self.net = NeuralNet(inp, hid, out)
        self.best = List[Snake]
        self.averages = [0, 0, 0]
        self.file_path = os.path.join(os.path.dirname(__file__), "saves")

    def start_population(self, load: bool):
        list_snakes = []

        if load:
            ld_weights, data = self.load()
            for i in range(self.size):
                snake_i = Snake()

                snake_i.weights = ld_weights[i]
                list_snakes.append(snake_i)

            self.generation = int(data[0])
            self.records[0] = int(data[1])
            self.records[1] = int(data[2])
            self.records[2] = int(data[3])
            self.records[3] = int(data[4])

        else:
            for i in range(self.size):
                snake_i = Snake()
                snake_i.weights = self.net.generate_weights()
                list_snakes.append(snake_i)

        self.snakes: List[Snake] = list_snakes
        self.save_snakes: List[Snake] = list_snakes

    def show_best(self):
        weights = np.genfromtxt(f"{self.file_path}/best/weights.csv")
        self.snakes = [Snake(weights)]

    def new_generations(self):
        self.save_snakes = sorted(self.snakes)
        self.plot.append([self.generation, self.save_snakes[0].fitness])

        if self.save_snakes[0].fitness > self.records[3]:
            self.records[0] = self.generation
            self.records[3] = self.save_snakes[0].fitness

        self.average()

        new_population = []
        for _ in range(self.size // 2):
            population = self.snakes.copy()

            parent_1 = self.ge.natural_selection(population)
            population.remove(parent_1)
            parent_2 = self.ge.natural_selection(population)

            offspring_1, offspring_2 = self.ge.crossover(
                parent_1.weights, parent_2.weights
            )
            offspring_1 = self.ge.mutation(offspring_1)
            offspring_2 = self.ge.mutation(offspring_2)

            new_population.append(Snake(offspring_1, 0))
            new_population.append(Snake(offspring_2, 0))

        self.snakes = new_population
        self.generation += 1

    def average(self):
        score = 0
        life_time = 0
        fitness = 0
        for snake in self.snakes:
            score += snake.score
            life_time += snake.life_time
            fitness += snake.fitness

        score /= self.size
        life_time /= self.size
        fitness /= self.size

        self.averages = [score, life_time, fitness]

    def get_high_score(self):
        return max(po.score for po in self.snakes)

    def get_high_life_time(self):
        return max(po.life_time for po in self.snakes)

    def get_high_fitness(self):
        return max(po.fitness for po in self.snakes)

    def save(self):
        weights = []
        data = np.array(
            [
                self.generation,
                self.records[0],
                self.records[1],
                self.records[2],
                self.records[3],
            ]
        )
        for snake in self.save_snakes:
            weights.append(snake.weights)

        weights = np.matrix(weights)
        np.savetxt(f"{self.file_path}/weights.csv", weights)
        np.savetxt(f"{self.file_path}/data.csv", data)
        with open(f"{self.file_path}/plot.csv", "ab") as f:
            np.savetxt(f, np.asarray(self.plot), delimiter=",")

    def load(self):
        weights = np.genfromtxt(f"{self.file_path}/weights.csv")
        data = np.genfromtxt(f"{self.file_path}/data.csv")
        return weights, data
