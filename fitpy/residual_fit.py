import inspect
import datetime

import logging

import end_conditions

log = logging.getLogger('fitpy.residual_fit')

def residual_fit(target_function, x_values, y_values,
                 y_stds=None,
                 residual='chi_squared',
                 parameter_constraints=None,
                 initial_guess=None,
                 max_evaluations=100000,
                 max_runtime=datetime.timedelta(minutes=5),
                 fit_tolerance=None,
                 verbosity=None,
                 log=None):
    '''
    Important DOCSTRING.
    '''
# setup logging (using verbosity)
# clean up input
    # verify target function is callable
    # make sure x values and y values have same length
# construct parameters - figure out how many, and what constraints
# construct algorithm
    # build end_conditions objects
    # build algorithm object
# perform fit
# cleanup
    # reset logging state if set by verbosity
# return results


# setup logging (using verbosity)
    if not log:
        log = logging.getLogger('fitpy.residual_fit')
    if vebosity:
        fplog = logging.getLogger('fitpy')
        old_logging_level = fplog.getEffectiveLevel()
        fplog.setLevel(verbosity)
# clean up input
    log.debug('Verifying input.')
    # verify target function is callable
    # make sure x values and y values have same length

# Consolodate parameter information
    log.debug('Determining number and names of parameters.')
    # Get names of the target_function's parameters.
    parameter_names = inspect.getargspec(target_function).args[1:]
    num_parameters = len(parameter_names)
    log.info('Found %d parameters in target function.' % num_parameters)

    # Make sure we have an appropriate set of constraints.
    parameter_constraint_list = []
    if parameter_constraints:
        log.debug('Found parameter constraints.')
        if isinstance(parameter_constraints, dict):
            for pn in parameter_names:
                try:
                    parameter_constraint_list.append(parameter_constraints[pn])
                except KeyError:
                    parameter_constraint_list.append(None)
        else:
            parameter_constraint_list = parameter_constraints
        assert(len(parameter_constraint_list) == num_parameters)

    # Make sure initial guess look good.
    initial_guess_list = []
    if initial_guess:
        log.debug('Found initial parameter guess.')
        if isinstance(initial_guess, dict):
            for pn in parameter_names:
                try:
                    initial_guess_list.append(initial_guess[pn])
                except KeyError:
                    initial_guess_list.append(None)
        else:
            initial_guess_list = initial_guess
        assert(len(initial_guess_list) == num_parameters)

# construct algorithm
    # Build fitness function/evaluation object
    log.debug('Build fitness function.')
    fit_func = residual_fitness_function(target_function, x_values, y_values,
                                         y_stds)
    # build end_conditions objects
    log.debug('Building end conditions.')
    ecs = simple_end_conditions(max_evaluations, max_runtime, fit_tolerance)
    # build algorithm object
    log.debug('Building algorithm object.')
    fitting_algorithm = construct_genetic_algorithm(fit_func,
                            parameter_constraint_list, ecs)
# perform fit
    log.info('Beginning fit.')
    best_parameters, best_residual = fitting_algorithm.run(initial_guess_list)
    log.info('Fit complete: best residual %f.' % best_residual)
# cleanup
    # reset logging state if set by verbosity
    if verbosity:
        fplog.setLevel(old_logging_level)
# return results
    return best_parameters, best_residual
