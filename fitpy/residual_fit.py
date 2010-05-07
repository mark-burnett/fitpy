import inspect
import collections

import logging

from .util.parameters import format_as_list
from .algorithms import factories

from .settings import *

__all__ = ['residual_fit']

log = logging.getLogger('fitpy.residual_fit')

def residual_fit(target_function, x_values, y_values,
                 y_stds=None,
                 residual_name=DEFAULT_RESIDUAL_NAME,
                 parameter_constraints=None,
                 initial_guess=None,
                 max_evaluations=DEFAULT_MAX_EVALUATIONS,
                 max_runtime=DEFAULT_MAX_RUNTIME,
                 fit_tolerance=None,
                 verbosity=None,
                 algorithm_name=DEFAULT_ALGORITHM_NAME,
                 **kwargs):
    '''
        Convenience function that finds a reasonable fit to x, y data using
    'target_function'
    '''
    # Function overview
    # -------------------------------------------------------------------
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

    # Setup logging (using verbosity)
    # -------------------------------------------------------------------
    log = logging.getLogger('fitpy.residual_fit')
    if verbosity:
        fplog = logging.getLogger('fitpy')
        old_logging_level = fplog.getEffectiveLevel()
        fplog.setLevel(verbosity)

    # Clean up input
    # -------------------------------------------------------------------
    log.debug('Verifying input.')
    # Verify target function is callable
    if not isinstance(target_function, collections.Callable):
        log.critical(
         'target_function must be a function or object with a __call__ method.')
        raise TypeError('target_function is not callable.')
    # Make sure x_values and y_values have same length
    if not len(x_values) == len(y_values):
        log.critical('length of x_values and y_values must be equal.')
        raise ValueError('Length of x_values and y_values not equal.')

    # Consolodate parameter information
    # -------------------------------------------------------------------
    # Get names of the target_function's parameters.
    log.debug('Determining number and names of parameters.')
    parameter_names = inspect.getargspec(target_function).args[1:]
    num_parameters  = len(parameter_names)
    log.info('Found %d parameter(s) in target function.' % num_parameters)

    # Accept parameter constrains as either a dictionary or list.
    parameter_constraint_list = format_as_list(
                                    parameter_constraints, parameter_names)

    # Accept initial guess as either a dictionary or a list.
    initial_guess_list = format_as_list(initial_guess, parameter_names)

    # Construct algorithm
    # -------------------------------------------------------------------
    # Build fitness function/evaluation object
    log.debug('Building fitness function.')
    fit_func = factories.make_residual_fitness_function(target_function,
                                                        x_values, y_values,
                                                        y_stds, residual_name,
                                                        **kwargs)
    # Build end_conditions objects
    log.debug('Building end conditions.')
# XXX do something special with tolerance stuff.
#    if fit_tolerance is None:
#        fit_tolerance = float(len(x_values))/2
    ecs = factories.make_simple_end_conditions(max_evaluations, max_runtime,
                                               fit_tolerance, **kwargs)
    # Build algorithm object
    log.debug('Building algorithm object.')
    fitting_algorithm = factories.make_algorithm(fit_func,
                                                 parameter_constraint_list,
                                                 ecs, algorithm_name,
                                                 **kwargs)

    # Perform fit
    # -------------------------------------------------------------------
    log.info('Beginning fit.')
    result = fitting_algorithm.run(initial_guess_list, **kwargs)

    log.info('Fit complete: best residual %f.' % result['best_residual'])

    # Cleanup
    # -------------------------------------------------------------------

    # Reset logging state if set by verbosity
    if verbosity:
        fplog.setLevel(old_logging_level)

    return result
