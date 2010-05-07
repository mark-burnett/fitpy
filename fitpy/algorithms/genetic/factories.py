import math

from . import strategies
from . import rankings
from . import reproduction

from .settings import *

from fitpy.utils import meshes

__all__ = ['make_algorithm']

def make_algorithm(fit_func, parameter_constraint_list, ecs, **kwargs):
    # 1) get a ranking function
    ranking_function = rankings.general
    # 2) make a reproduction object based on the parameter constraints
    # this function returns a reproduction 
    #     object based on parameter constraints.
    reproduction_object = make_default_reproduction(parameter_constraint_list,
                                                    **kwargs)
    # 3) string together a bunch of objects into the algorithm
    return strategies.GeneticAlgorithm(fit_func, ranking_function, 
                                       reproduction_object, ecs)

def make_default_reproduction(parameter_constraint_list, 
                              crossover_rate=DEFAULT_CROSSOVER_RATE, 
                              mutation_rate=DEFAULT_MUTATION_RATE,
                              perturbation_rate=DEFAULT_PERTURBATION_RATE,
                              num_points=DEFAULT_NUMBER_SAMPLE_POINTS,
                              **kwargs):
    """
    Inputs:
        parameter_constraint_list   : A list of tuples which
                                      give bounds on parameters
      --kwargs--
        crossover_rate              : how likely the reproduction swaps
                                      gene sequences (see glossary)
        mutation_rate               : how likely any individual parameter
                                      will take on a completely random value
        purterbation_rate           : how likely any idividual parameter
                                      will slightly change.
        num_points                  : Number of values chosen between bounds
                                      for each parameter.
    Returns:
        reproduction_object
    """
    allowed_parameter_values = []
    # determine the allowed parameter values
    for lower, upper in parameter_constraint_list:
        # figure out the mesh details
        if math.log(upper-lower, 10) > 3.0:
            # if the constraints vary over more than 3 orders...
            mesh = meshes.logmesh(lower, upper, num_points)
        else:
            mesh = meshes.linmesh(lower,upper, num_points)
        allowed_parameter_values.append(mesh)    

    # return basic constrained reproduction
    return reproduction.DiscreteStandard(allowed_parameter_values, 
                                         crossover_rate,
                                         mutation_rate,
                                         perturbation_rate)
