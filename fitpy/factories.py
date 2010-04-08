from residuals import residual_functions
import end_conditions

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
    pass
