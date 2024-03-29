import inspect
import itertools
import collections
import logging

from .utils import logutils

from .utils.parameters import format_as_list
from .utils import funcutils
from .algorithms import factories

import default_settings as ds

logger = logutils.getLogger(__file__)

def optimize(cost_function,
             parameter_constraints=None,
             initial_guess=None,
             max_evaluations=ds.MAX_EVALUATIONS,
             max_runtime=ds.MAX_RUNTIME,
             target_cost=None,
             verbosity=None,
             algorithm_name=ds.ALGORITHM_NAME,
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
    if verbosity:
        # find out the logging level of highest level logger and remember it.
        fplog = logging.getLogger('fitpy')
        old_logging_level = fplog.getEffectiveLevel()
        # this setting will percolate down to lower level loggers.
        fplog.setLevel(verbosity)

    # Clean up input
    # -------------------------------------------------------------------
    logger.debug('Verifying input.')
    # Verify cost function is callable
    if not isinstance(cost_function, collections.Callable):
        logger.critical(
         'cost_function must be a function or object with a __call__ method.')
        raise TypeError('cost_function is not callable.')

    # Consolodate parameter information
    # -------------------------------------------------------------------
    # Get names of the target_function's parameters.
    logger.debug('Determining number and names of parameters.')
    parameter_names = funcutils.get_parameter_names(cost_function)
    num_parameters  = len(parameter_names)
    logger.info('Found %d parameter(s) in target function.' % num_parameters)

    # Accept parameter constrains as either a dictionary or list.
    parameter_constraint_list = format_as_list(
                                    parameter_constraints, parameter_names)

    # Accept initial guess as either a dictionary or a list.
    initial_guess_list = format_as_list(initial_guess, parameter_names)

    # Construct algorithm
    # -------------------------------------------------------------------
    # Build end_conditions objects
    logger.debug('Building end conditions.')
    ecs = factories.make_simple_end_conditions(max_evaluations, max_runtime,
                                               target_cost, **kwargs)
    # Build algorithm object
    logger.debug('Building algorithm object.')
    fitting_algorithm = factories.make_algorithm(cost_function,
                                                 parameter_constraint_list,
                                                 ecs, algorithm_name,
                                                 **kwargs)

    # Perform fit
    # -------------------------------------------------------------------
    logger.info('Beginning fit.')
    result = fitting_algorithm.run(initial_guess_list, **kwargs)

    best_parameters = result['best_parameters']
    logger.info('Fit complete: best cost %f.' % 
                result['evaluation_cache'][best_parameters])
    for name, value in itertools.izip(parameter_names, best_parameters):
        logger.info('%s = % f' % (name, value))

    # Cleanup
    # -------------------------------------------------------------------

    # Reset logging state if set by verbosity
    if verbosity:
        fplog.setLevel(old_logging_level)

    return result
