import numpy as np
import random


class Genetic:
    def natural_selection(self, population):
        fitness_sum = sum([c.fitness for c in population])
        selection_probes = [c.fitness / fitness_sum for c in population]
        parent = population[np.random.choice(len(population), p=selection_probes)]
        return parent

    def crossover(self, parent_1, parent_2):
        point_selected = random.randint(10, len(parent_1) // 2)
        offspring_1 = np.concatenate(
            (parent_1[:point_selected], parent_2[point_selected:])
        )
        offspring_2 = np.concatenate(
            (parent_2[:point_selected], parent_1[point_selected:])
        )

        return offspring_1, offspring_2

    def mutation(self, offspring):
        for i in range(len(offspring)):
            if np.random.random() < 0.01:
                offspring[i] = np.random.normal(0, 1 / 4)

        return offspring
