from fitpy.algorithm import common
from fitpy.algorithm import algorithm_names

def make_residual_fitness_function(target_function,
                                   x_values, y_values, y_stds,
                                   residual_name):
    residual_function = common.residuals.residual_functions[residual_name.lower()]
    def residual_fitness_function(parameters):
        return residual_function(x_values, y_values, y_stds,
                                 target_function(x_values, *parameters))

    return residual_fitness_function

def make_simple_end_conditions(max_evaluations, max_runtime,
                               fit_tolerance):
    return [common.end_conditions.MaxEvaluations(max_evaluations),
            common.end_conditions.MaxRuntime(max_runtime),
            common.end_conditions.FitTolerance(fit_tolerance)]

def make_algorithm(fit_func, parameter_constraint_list, ecs, algorithm_name):
    if not algorithm_name in algorithm_names:
        raise RuntimeError('Illegal algorithm name, %s.  Must be one of: %s' %
                           (algorithm_name, str(algorithm_names)))
    # Import the algorithm module, and instantiate the algorithm.
    exec('import ' + algorithm_name)
    module = eval(algorithm_name)
    return module.factories.make_algorithm(fit_func, parameter_constraint_list,
                                           ecs)
