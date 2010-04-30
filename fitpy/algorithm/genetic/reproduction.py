import random
import logging

import util

log = logging.getLogger('fitpy.reproduction.reproduction_objects')

class DiscreteStandard(object):
    def __init__(self, allowed_parameter_values,
                 crossover_rate, mutation_rate,
                 perturbation_rate):
        self.allowed_parameter_values = allowed_parameter_values
        self.crossover_rate    = crossover_rate
        self.mutation_rate     = mutation_rate
        self.perturbation_rate = perturbation_rate

    def generate_children(self, parents, generation_size, elite_size, pop):
        """
        Generates the next generation from population.
        """
        num_children = generation_size - elite_size
        children = []
        while len(children) < num_children:
            # Choose parents
            p1, p2 = util.select_parents(parents)

            # Create potential children
            c1, c2 = util.binary_crossover(p1, p2, self.crossover_rate)
            c1 = util.discrete_mutation(c1, self.mutation_rate,
                                        self.allowed_parameter_values)
            c2 = util.discrete_mutation(c2, self.mutation_rate,
                                        self.allowed_parameter_values)
            c1 = tuple(util.discrete_perturbation(c1, self.perturbation_rate,
                                                 self.allowed_parameter_values))
            c2 = tuple(util.discrete_perturbation(c2, self.perturbation_rate,
                                                 self.allowed_parameter_values))
            
            # Add unique children to next generation
            if c1 not in pop and c1 not in children:
                children.append(c1)
            else:
                log.debug('Created non-unique child.')

            if len(children) >= num_children:
                log.debug('Created unnecessary child.')
            elif c2 in pop or c2 in children:
                log.debug('Created non-unique child.')
            else:
                children.append(c2)

        return children, parents[:elite_size]

    def random_generation(self, generation_size):
        """
        Generate a legal random population of 'generation_size'.
        """
        return [tuple(random.choice(self.allowed_parameter_values[i])
                      for i in xrange(len(self.allowed_parameter_values)))
                for n in xrange(generation_size)]
