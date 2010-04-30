from residuals import residual_functions
import end_conditions
import ranking
import reproduction.factories
import algorithm

__all__ = ['make_residual_fitness_function',
           'make_simple_end_conditions',
           'make_genetic_algorithm']

def make_residual_fitness_function(target_function,
                                   x_values, y_values, y_stds,
                                   residual):
    residual_function = residual_functions[residual.lower()]
    def residual_fitness_function(parameters):
        return residual_function(x_values, y_values, y_stds,
                                 target_function(x_values, *parameters))

    return residual_fitness_function

def make_simple_end_conditions(max_evaluations, max_runtime,
                               fit_tolerance):
    return [end_conditions.MaxEvaluations(max_evaluations),
            end_conditions.MaxRuntime(max_runtime),
            end_conditions.FitTolerance(fit_tolerance)]

def make_genetic_algorithm(fit_func, parameter_constraint_list, ecs):
    # 1) get a ranking function
    ranking_function = ranking.general
    # 2) make a reproduction object based on the parameter constraints
    # this function returns a reproduction 
    #     object based on parameter constraints.
    reproduction_object = reproduction.factories.default_reproduction(
                                                 parameter_constraint_list)
    # 3) string together a bunch of objects into the algorithm
    return algorithm.GeneticAlgorithm(fit_func, ranking_function, 
                                                      reproduction_object, ecs)

import math

from fitpy.settings import * # all default settings will be in all caps.
import fitpy.meshes as meshes
import reproduction_objects

def default_reproduction(parameter_constraint_list, 
                         crossover_rate=DEFAULT_CROSSOVER_RATE, 
                         mutation_rate=DEFAULT_MUTATION_RATE,
                         perturbation_rate=DEFAULT_PERTURBATION_RATE,
                         num_points=DEFAULT_NUMBER_SAMPLE_POINTS):
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
    # find out if any parameters have no constraints
    for constraint in parameter_constraint_list:
        if constraint is None:
            # hand off to more flexible reproduction
            raise NotImplementedError()
            
    allowed_parameter_values = []
    # determine the allowed parameter values
    for lower,upper in parameter_constraint_list:
        # figure out the mesh details
        if math.log(upper-lower, 10) > 3.0:
            # if the constraints vary over more than 3 orders...
            mesh = meshes.logmesh(lower, upper, num_points)
        else:
            mesh = meshes.linmesh(lower,upper, num_points)
        allowed_parameter_values.append(mesh)    

    # return basic constrained reproduction
    return reproduction_objects.DiscreteStandard(allowed_parameter_values, 
                                                 crossover_rate,
                                                 mutation_rate,
                                                 perturbation_rate)
