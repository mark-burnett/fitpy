import logging
import itertools

log = logging.getLogger('fitpy.algorithm')

__all__ = ['GeneticAlgorithm']

class Population(object):
    def __init__(self):
        self.generations = []
        self.fitnesses   = []
        self._cache      = {}

    def __contains__(self, individual):
        return individual in self._cache

    def add_generation(self, generation, fitnesses):
        for i, f, in itertools.izip(generation, fitnesses):
            self._cache[i] = f
        self.generations.append(generation)
        self.fitnesses.append(fitnesses)

    def get_fitness(self, i):
        return self._cache[i]
