import itertools

from ..common.evaluation_cache import EvaluationCache


class Population(EvaluationCache):
    def __init__(self):
        EvaluationCache.__init__(self)
        self.generations = []

    def add_generation(self, generation, fitnesses):
        for i, f, in itertools.izip(generation, fitnesses):
            self[i] = f
        self.generations.append(generation)

