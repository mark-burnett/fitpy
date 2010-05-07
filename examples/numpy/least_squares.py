import numpy
import random

import fitpy

# Here's the functional form we will fit
def functional_form(x, a, b, c):
    """
    par is a sequence of parameters (a chromosome in the fitting algorithm)

    x is where to evaluate the function
    """
    return a * numpy.exp(b * x) + c

# Generate some noisy data to fit
target_parameters = (3.16, -0.478, 2.105)

data_size = 1000
xmin      = 0
xmax      = 25

x    = numpy.linspace(xmin, xmax, data_size)
data = functional_form(x, *target_parameters) + (numpy.random.random(data_size) - 0.5)

# Perform the fit
fit_results = fitpy.residual_fit(functional_form, x, data, 
                                 parameter_constraints= {'a':(-5, 5), 
                                                         'b':(-5, 5), 
                                                         'c':(-5, 5)}, 
                                 verbosity=10, # FIXME remove after testing...
                                 max_evaluations=5000)
fit_parameters = fit_results['best_parameters']
chi_squared    = fit_results['best_residual']

# Show the result of the fit
print 'Chi-squared per datum:', chi_squared/data_size
print 'Percent errors for the fit parameters:'
print [(f - t)/t for f, t in zip(fit_parameters, target_parameters)]

try: # in case the users don't have matplotlib installed on the system.
    import pylab

    pylab.plot(x, data, linewidth = 2, color='black', label='Data')
    pylab.plot(x, functional_form(x, *fit_parameters), color='red', label='Fit')
    pylab.legend()
    pylab.title("Least squares fitting example.")
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.show()
except ImportError:
    pass
