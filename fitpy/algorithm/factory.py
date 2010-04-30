from fitpy.algorithm import common

def make_residual_fitness_function(target_function,
                                   x_values, y_values, y_stds,
                                   residual_name):
    residual_function = common.residual.residual_functions[residual_name.lower()]
    def residual_fitness_function(parameters):
        return residual_function(x_values, y_values, y_stds,
                                 target_function(x_values, *parameters))

    return residual_fitness_function

def make_simple_end_conditions(max_evaluations, max_runtime,
                               fit_tolerance):
    return [common.end_conditions.MaxEvaluations(max_evaluations),
            common.end_conditions.MaxRuntime(max_runtime),
            common.end_conditions.FitTolerance(fit_tolerance)]
