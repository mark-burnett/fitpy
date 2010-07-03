from . import common
from .algorithm_names import algorithm_names

from fitpy.utils.cost_function_wrapper import CostFunctionWrapper
from fitpy.utils.funcutils import get_parameter_names

def make_residual_cost_function(target_function,
                                x_values, y_values, y_errors,
                                residual_name,
                                **kwargs):
    residual_function = common.residuals.residual_functions[
                            residual_name.lower()]

    def residual_cost_function(*parameters):
        return residual_function(x_values, y_values, y_errors,
                                 target_function(x_values, *parameters),
                                 **kwargs)

    parameter_names = get_parameter_names(target_function)
    # Throw away 'x' part of target_function arguments
    parameter_names = parameter_names[1:]
    return CostFunctionWrapper(residual_cost_function, parameter_names)

def make_simple_end_conditions(max_evaluations, max_runtime,
                               target_cost, **kwargs):
    ecs = []
    if max_evaluations is not None:
        ecs.append(common.end_conditions.MaxEvaluations(max_evaluations))
    if max_runtime is not None:
        ecs.append(common.end_conditions.MaxRuntime(max_runtime))

    if target_cost is not None:
        ecs.append(common.end_conditions.MinimumCost(target_cost))

    return ecs

def make_algorithm(cost_func, parameter_constraint_list, end_conditions,
                   algorithm_name, **kwargs):
    if not algorithm_name in algorithm_names:
        raise RuntimeError('Illegal algorithm name, %s.  Must be one of: %s' %
                           (algorithm_name, str(algorithm_names)))
    # Import the algorithm module, and instantiate the algorithm.
    exec('import ' + algorithm_name)
    module = eval(algorithm_name)
    return module.factories.make_algorithm(cost_func, parameter_constraint_list,
                                           end_conditions, **kwargs)
