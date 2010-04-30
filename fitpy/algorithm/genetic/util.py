import copy
import random

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
        
def select_parents(ranked_population):
    """
    Picks 2 parents from the ranked_population
    """
    p1 = weighted_choice(ranked_population)
    p2 = p1
    while p1 == p2:
        p2 = weighted_choice(ranked_population)
    return p1, p2

def weighted_choice(population, width=None):
    """
        Choose a random element from population, weighted toward the
    front of the list.
    """
    if not width:
        width = float(len(population))/2
    j = len(population)
    while j >= len(population):
        j = abs(int(random.normalvariate(0, width)))
    return population[j]
