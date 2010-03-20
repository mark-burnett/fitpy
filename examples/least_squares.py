import numpy

import fitpy

# Here's the functional form we will fit
def functional_form(x, par):
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

x    = numpy.linspace(xmin, xmax, data_size)
data = functional_form(target_parameters, xmesh)\
     + numpy.random.normal(size=data_size)

# Perform the fit
fit_parameters, chisquared = fitpy.least_squares(functional_form, x, data)

# Show the result of the fit
print 'Chi-squared per datum:', chisquared/data_size
print 'Percent errors for the fit parameters:'
print [(f - t)/t for f, t in zip(fit_parameters, target_parameters)]
