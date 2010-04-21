import logging
import itertools

from fitpy.settings import *

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

class GeneticAlgorithm(object):
    def __init__(self, fitness_func, rank, reproduce, end,
                 generation_size=DEFAULT_GENERATION_SIZE,
                 elite_size=DEFAULT_ELITE_SIZE):
        self.fitness_func    = fitness_func
        self.rank            = rank
        self.reproduce       = reproduce
        self.end             = end
        self.generation_size = generation_size
        self.elite_size      = elite_size

    def get_initial_generation(self, initial_guess_list):
        if any(initial_guess_list):
            raise NotImplementedError('Initial guesses not allowed.')
        return self.reproduce.random_generation(self.generation_size)

    def run(self, initial_generation):
        # Initialze the run
        pop = Population()

        log.debug('Evaluating initial generation.')
        initial_fitnesses = [self.fitness_func(i) for i in initial_generation]
        ranked_gen, ranked_fitnesses = self.rank(initial_generation,
                                                 initial_fitnesses)
        num_evaluations = len(ranked_gen)

        pop.add_generation(ranked_gen, ranked_fitnesses)

        best         = pop.generations[-1][0]
        best_fitness = pop.fitnesses[-1][0]

        [e.reset() for e in self.end]
        var = locals()
        while not any(e(var) for e in self.end):
            # Generate children
            log.debug('Generating individuals for generation %d.'
                        % len(pop.generations))
            children, elites   = self.reproduce.generate_children(
                                    ranked_gen, self.generation_size,
                                    self.elite_size, pop)

            # Evaluate children
            log.debug('Evaluating generation %d.'
                        % len(pop.generations))
            children_fitnesses = [self.fitness_func(c) for c in children]
            elite_fitnesses    = ranked_fitnesses[:self.elite_size]

            # Rank the generation
            log.debug('Ranking generation %d.'
                        % len(pop.generations))
            ranked_gen, ranked_fitnesses = self.rank(children + elites,
                                                     children_fitnesses + 
                                                     elite_fitnesses)
            # Store generation
            log.debug('Storing generation %d.'
                        % len(pop.generations))
            pop.add_generation(ranked_gen, ranked_fitnesses)

            # Progress tracking
            best             = pop.generations[-1][0]
            best_fitness     = pop.fitnesses[-1][0]
            num_evaluations += len(children)

        # Return
        return pop
