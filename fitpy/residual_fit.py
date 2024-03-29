import inspect
import itertools
import collections
import logging

from .utils import logutils

from .utils.parameters import format_as_list
from .algorithms import factories

import default_settings as ds

from .optimize import optimize

__all__ = ['residual_fit']

logger = logutils.getLogger(__file__)

# XXX rename target_function to model_function (don't forget docs)
def residual_fit(target_function, x_values, y_values,
                 y_errors=None,
                 residual_name=ds.RESIDUAL_NAME,
                 parameter_constraints=None,
                 initial_guess=None,
                 max_evaluations=ds.MAX_EVALUATIONS,
                 max_runtime=ds.MAX_RUNTIME,
                 target_residual=None,
                 verbosity=None,
                 algorithm_name=ds.ALGORITHM_NAME,
                 **kwargs):
    '''
        Convenience function that finds a reasonable fit to x, y data using
    'target_function'
    '''
    if verbosity:
        # find out the logging level of highest level logger and remember it.
        fplog = logging.getLogger('fitpy')
        old_logging_level = fplog.getEffectiveLevel()
        # this setting will percolate down to lower level loggers.
        fplog.setLevel(verbosity)

    # Clean up input
    # -------------------------------------------------------------------
    logger.debug('Verifying input.')
    # Verify target function is callable
    if not isinstance(target_function, collections.Callable):
        logger.critical(
         'target_function must be a function or object with a __call__ method.')
        raise TypeError('target_function is not callable.')
    # Make sure x_values and y_values have same length
    if not len(x_values) == len(y_values):
        logger.critical('length of x_values and y_values must be equal.')
        raise ValueError('Length of x_values and y_values not equal.')

    logger.debug('Building cost function.')
    cost_func = factories.make_residual_cost_function(target_function,
                                                      x_values, y_values,
                                                      y_errors, residual_name,
                                                      **kwargs)

    result = optimize(cost_func,
                      parameter_constraints=parameter_constraints,
                      initial_guess=initial_guess,
                      max_evaluations=max_evaluations,
                      max_runtime=max_runtime,
                      target_cost=target_residual,
                      verbosity=None,
                      algorithm_name=algorithm_name,
                      **kwargs)

    # Reset logging state if set by verbosity
    if verbosity:
        fplog.setLevel(old_logging_level)
    return result
