from fitpy.utils import logutils

from ..common.evaluation_cache import EvaluationCache
from .settings import DEFAULT_INITIAL_POPULATION_SIZE

logger = logutils.getLogger(__file__)

__all__ = ['GeneticAlgorithm']

class GeneticAlgorithm(object):
    def __init__(self, fitness_func, population, reproduce, end, **kwargs):
        self.fitness_func    = fitness_func
        self.population      = population
        self.reproduce       = reproduce
        self.end             = end

    def run(self, initial_guess_list,
            initial_population_size=DEFAULT_INITIAL_POPULATION_SIZE, **kwargs):
        # Initialze the run
        initial_parameters_set = self.reproduce.random_set(initial_population_size,
                                                           initial_guess_list)

        evaluation_cache = EvaluationCache()
        for p in self.population:
            evaluation_cache[p.parameters] = p.fitness

        num_evaluations = len(evaluation_cache)

        logger.debug('Evaluating initial generation.')
        for parameters in initial_parameters_set:
            fitness = self.fitness_func(parameters)
            evaluation_cache[parameters] = fitness
            self.population.add(parameters, fitness)
            num_evaluations += 1

        best_parameters = self.population[0].parameters
        best_fitness    = self.population[0].fitness

        for e in self.end:
            e.reset()

        ec_locals = locals()
        while not any(e(ec_locals) for e in self.end):
            # Generate children
            child = self.reproduce.generate_child(self.population,
                                                  evaluation_cache)
            fitness = self.fitness_func(child)
            evaluation_cache[child] = fitness
            self.population.add(child, fitness)

            # Progress tracking
            best_parameters = self.population[0].parameters
            best_fitness    = self.population[0].fitness
            num_evaluations += 1
            ec_locals = locals()

        # Return
        return {'evaluation_cache': evaluation_cache,
                'best_parameters':  best_parameters,
                'best_fitness':     best_fitness}
