import itertools

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
    def __init__(self, fitness_func, rank, reproduce, end):
        self.fitness_func = fitness_func
        self.rank         = rank
        self.reproduce    = reproduce
        self.end          = end

    def run(self, initial_population):
        # Initialze the run
        pop = Population()

        initial_fitnesses = [self.fitness_func(*i) for i in initial_population]
        ranked_gen, ranked_fitnesses = self.rank(initial_population,
                                                 initial_fitnesses)
        num_evaluations = len(ranked_gen)

        pop.add_generation(ranked_gen, ranked_fitnesses)

        [e.reset() for e in self.end]
        while not any(e(locals()) for e in self.end):
            # Generate children
            children, elites   = self.reproduce(ranked_gen, pop)

            # Evaluate children
            children_fitnesses = [self.fitness_func(*c) for c in children]
            elite_fitnesses    = [pop.get_fitness(i) for i in elites]

            # Rank the generation
            ranked_gen, ranked_fitnesses = self.rank(children + elites,
                                                     children_fitnesses + 
                                                     elite_fitnesses)
            # Store generation
            pop.add_generation(ranked_gen, ranked_fitnesses)

            # Progress tracking
            best             = pop.generations[-1][0]
            best_fitness     = pop.fitnesses[-1][0]
            num_evaluations += children

        # Return
        return pop
