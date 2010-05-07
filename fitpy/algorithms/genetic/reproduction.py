import copy
import random

from fitpy.util import logutils

from ..common import choice

logger = logutils.getLogger(__file__)

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
            p1, p2 = choice.choose_two(parents, choice.weighted_choice)

            # Create potential children
            c1, c2 = binary_crossover(p1, p2, self.crossover_rate)
            c1 = discrete_mutation(c1, self.mutation_rate,
                                   self.allowed_parameter_values)
            c2 = discrete_mutation(c2, self.mutation_rate,
                                   self.allowed_parameter_values)
            c1 = tuple(discrete_perturbation(c1, self.perturbation_rate,
                                            self.allowed_parameter_values))
            c2 = tuple(discrete_perturbation(c2, self.perturbation_rate,
                                            self.allowed_parameter_values))
            
            # Add unique children to next generation
            if c1 not in pop and c1 not in children:
                children.append(c1)
            else:
                logger.debug('Created non-unique child, %s.' % str(c1))

            if len(children) >= num_children:
                logger.debug('Created unnecessary child, %s.' % str(c2))
            elif c2 in pop or c2 in children:
                logger.debug('Created non-unique child, %s.' % str(c2))
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

def binary_crossover(a, b, rate):
    """
    Performs a normal crossover between a and b, generating 2 children.
    """
    c1 = []
    c2 = []
    switched = False
    for ai, bi in zip(a,b):
        if random.random() < rate:
            switched = not switched
        if switched:
            c1.append(bi)
            c2.append(ai)
        else:
            c1.append(ai)
            c2.append(bi)
    return c1, c2

def discrete_mutation(c, rate, allowed_values):
    """
    Performs mutation on c given self.mutation_rate.

    Uses a uniform distribution to pick new allel values.
    """
    m = copy.copy(c)
    for i in xrange(len(c)):
        if random.random() < rate:
            m[i] = random.choice(allowed_values[i])
    return m

def discrete_perturbation(individual, rate, allowed_values):
    """
    Randomly vary parameters to neighboring values given rate.
    """
    ind = copy.copy(individual)
    for par_index, par_value in enumerate(ind):
        r = random.random()
        if r < rate:
            value_index = allowed_values[par_index].index(par_value)
            if 0 == value_index:
                ind[par_index] = allowed_values[par_index][1]
            elif len(allowed_values[par_index]) - 1 == value_index:
                ind[par_index] = allowed_values[par_index][-2]
            else:
                if r < rate/2:
                    ind[par_index] = allowed_values[par_index][value_index - 1]
                else:
                    ind[par_index] = allowed_values[par_index][value_index + 1]
    return ind
