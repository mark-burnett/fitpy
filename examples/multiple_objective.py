import numpy

import fitpy
from fitpy.helpers import chi_squared, count_zero_crossings

# Here's the functional form we will fit
def functional_form(par, x):
    """
    par is a sequence of parameters (a chromosome in the fitting algorithm)

    x is where to evaluate the function
    """
    return par[0] * numpy.exp(par[1] * x * numpy.sin(par[2] * x)) + par[3]

# Generate some noisy data to fit.
target_parameters = (1.5, 2.73, 5.15, 0.3)

data_size = 500
xmin      = 0
xmax      = 10

xmesh    = numpy.linspace(xmin, xmax, data_size)
fit_data = functional_form(target_parameters, xmesh)\
         + numpy.random.normal(size=data_size)

fit_czc  = count_zero_crossings(fit_data - 1)

# Here is a fitness function that evaluates individuals using multiple objectives
delta = 1e-15
def fitness_function(chromosome):
    """
    Returns a tuple of fitnesses for the given chromosome.
    The objectives used are:
        overall least-squares fit.
        number of times crossing the line y = 1
        intial value y(x=0)
    """
    ymesh = functional_form(chromosome, xmesh)

    residual       = chi_squared(ymesh, fit_data)
    zero_crossings = count_zero_crossings(ymesh - 1)

    return (1.0/(delta + residual),
            1.0/(delta + (zero_crossings - fit_czc)**2),
            1.0/(delta + (ymesh[0] - fit_data[0])**2))

# Set constraints on parameters (alleles in genetic algorithm vocabulary).
allele_constraints = [(0.1, 10),
                      (0.1, 10),
                      (0.1, 10),
                      (0, 1000)]

fit_parameters, fitnesses = fitpy.multiple_objective(fitness_function,
                                                     allele_constraints)

# Show the result of the fit
print 'Final fitnesses:', fitnesses
print 'Percent errors for the fit parameters:'
print [(f - t)/t for f, t in zip(fit_parameters, target_parameters)]
