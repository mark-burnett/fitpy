from fitpy.utils import logutils

from ..common.evaluation_cache import EvaluationCache
from .settings import DEFAULT_INITIAL_POPULATION_SIZE

logger = logutils.getLogger(__file__)

__all__ = ['GeneticAlgorithm']

class GeneticAlgorithm(object):
    def __init__(self, cost_func, population, reproduce, end, **kwargs):
        self.cost_func    = cost_func
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
            evaluation_cache[p.parameters] = p.cost

        num_evaluations = len(evaluation_cache)

        logger.debug('Evaluating initial generation.')
        for parameters in initial_parameters_set:
            cost = self.cost_func(*parameters)
            evaluation_cache[parameters] = cost
            self.population.add(parameters, cost)
            num_evaluations += 1

        best_parameters = self.population[0].parameters
        best_cost    = self.population[0].cost

        for e in self.end:
            e.reset()

        ec_locals = locals()
        while not any(e(ec_locals) for e in self.end):
            # Generate children
            child = self.reproduce.generate_child(self.population,
                                                  evaluation_cache)
            cost = self.cost_func(*child)
            evaluation_cache[child] = cost
            self.population.add(child, cost)

            # Progress tracking
            best_parameters = self.population[0].parameters
            best_cost    = self.population[0].cost
            num_evaluations += 1
            ec_locals = locals()

        # Return
        return {'evaluation_cache': evaluation_cache,
                'best_parameters':  best_parameters,
                'best_cost':        best_cost}
