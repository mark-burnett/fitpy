import copy
import random

from fitpy.utils import logutils

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

    def generate_child(self, population, cache):
        """
        Generates a child.
        """
        child = None
        while not child:
            parent1, parent2 = choice.choose_two(population, choice.weighted_choice)

            child, unloved_child = binary_crossover(parent1.parameters,
                                                    parent2.parameters,
                                                    self.crossover_rate)
            child = discrete_mutation(child, self.mutation_rate,
                                      self.allowed_parameter_values)
            child = discrete_perturbation(child, self.perturbation_rate,
                                          self.allowed_parameter_values)

            # Allow hashing of child for use in dicts/sets.
            child = tuple(child)
            
            if child in cache or child in population:
                logger.debug('Created non-unique child, %s from parents: %s, %s.' % (str(child), str(parent1), str(parent2)))
                child = None

        return child

    def random_set(self, size, guess=None):
        """
        Generate a legal random population of 'generation_size'.
        """
        if guess:
            size -= 1

        generated = [tuple(random.choice(self.allowed_parameter_values[i])
                      for i in xrange(len(self.allowed_parameter_values)))
                     for n in xrange(size)]

        if guess:
            return [guess] + generated

        return generated

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
