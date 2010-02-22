from itertools import izip

__all__ = ['GeneticAlgorithm']

class GeneticAlgorithm(object):
    """
        Contains a template for performing a fairly general set of
    genetic algorithms.
    """
    def __init__(self, evaluate, rank, reproduce, end):
        """
        evaluate:  Callabe that returns a fitness for a given chromosome.
        rank:      Callable that returns a population sorted by fitness.
        reproduce: Object that generates the next and intial generations
        end:       Sequence of end conditions.  Stops when any is true.
        """
        self.evaluate  = evaluate
        self.rank      = rank
        self.reproduce = reproduce
        self.end       = end
        self.cache     = {}

    def fit(self, population_size, initial_population_size, elite_size):
        assert(initial_population_size >= population_size)
        assert(elite_size < population_size)
        assert(elite_size >= 0)

        # Reset end conditions
        # NOTE: Ranking a large initial population can be expensive, so
        #       this might be the best place to reset timers, etc.
        [e.reset() for e in self.end]

        # Generate and rank initial population
        initial_population = self.reproduce.random_population(initial_population_size)
        add_to_cache(initial_population, self.evaluate(initial_population), self.cache)
        ranked_initial_population = self.rank(initial_population, self.cache)

        # Gather our first real generation
        ranked_population = ranked_initial_population[:population_size]
        elites            = ranked_initial_population[:elite_size]

        # History and progress tracking
        self.generations = [ranked_population]
        best             = ranked_population[0]
        best_fitness     = self.cache[best]

        # Loop until any end condition is satisfied
        while not any(e(best_fitness) for e in self.end):
            # Reproduce
            children = self.reproduce(ranked_population, self.cache)

            # Evaluate
            add_to_cache(children, self.evaluate(children), self.cache)

            # Rank
            ranked_children   = self.rank(children + elites, self.cache)
            elites            = ranked_children[:elite_size]
            ranked_population = ranked_children[:population_size]

            # History and progress tracking
            self.generations.append(ranked_population)
            best         = ranked_population[0]
            best_fitness = self.cache[best]

        return best, best_fitness

def add_to_cache(keys, values, cache):
    for k, v in izip(keys, values):
        cache[k] = v
