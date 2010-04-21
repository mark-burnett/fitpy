import logging
import datetime

import numpy
import residual_fit

def target_function(x, a, b):
    return a*x + b

x_values = numpy.array([x for x in range(10)])
y_values = target_function(x_values, 1.6, -4.3)

residual_fit.residual_fit(target_function, x_values, y_values, 
                          parameter_constraints=[[-10,10],[-10,10]],
                          max_runtime=datetime.timedelta(seconds=5),
                          verbosity=logging.DEBUG)
