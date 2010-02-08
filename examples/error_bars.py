from itertools import izip

import numpy

import fitpy

# Here's the functional form we will fit
def functional_form(par, x):
    """
    par is a sequence of parameters (a chromosome in the fitting algorithm)

    x is where to evaluate the function
    """
    return par[0] * numpy.exp(par[1] * x) + par[2]

# Generate some noisy data to fit
target_parameters = (3.16, -0.478, 2.105)

data_size = 1000
xmin      = 0
xmax      = 25

x = numpy.linspace(xmin, xmax, data_size)

perfect_data   = functional_form(target_parameters, x)
std_deviations = numpy.random.uniform(0.01, 0.3, data_size) *\
                 perfect_data
fit_data       = numpy.array(p + scipy.random.normal(scale=s)
                             for p, s in izip(perfect_data, std_deviations))

# Perform the fit
fit_parameters, chisquared = fitpy.least_squares(functional_form, x,
                                                 fit_data,
                                                 error_estimates=std_deviations)

# Show the result of the fit
print 'Normalized chi-squared per datum:', chisquared/data_size
print 'Percent errors for the fit parameters:'
print [(f - t)/t for f, t in zip(fit_parameters, target_parameters)]
