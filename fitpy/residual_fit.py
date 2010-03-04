import inspect
import datetime

def residual_fit(target_function, x_values, y_values,
                 y_stds=None,
                 residual='chi_squared',
                 parameter_constraints=None,
                 initial_guess=None,
                 max_evaluations=100000,
                 max_runtime=datetime.timedelta(minutes=5),
                 fit_tolerance=None,
                 verbosity=3):
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
# clean up input
    # verify target function is callable
    # make sure x values and y values have same length

# Consolodate parameter information
    # Get names of the target_function's parameters.
    parameter_names = inspect.getargspec(target_function).args[1:]
    num_parameters = len(parameter_names)

    # Make sure we have an appropriate set of constraints.
    parameter_constraint_list = []
    if parameter_constraints:
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
    # build end_conditions objects
    # build algorithm object
    fitting_algorithm = construct_genetic_algorithm(target_function,
                            evaluation_guy(residual), parameters_info,
                            end_conditions)
# perform fit
# cleanup
    # reset logging state if set by verbosity
# return results
