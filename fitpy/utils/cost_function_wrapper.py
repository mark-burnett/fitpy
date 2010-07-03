# XXX Consider making this into a ResidualCostFunction object
# and moving the residual closure from the factory into it.
class CostFunctionWrapper(object):
    def __init__(self, function, parameter_names):
        self.function = function
        self.parameter_names = parameter_names

    def __call__(self, *args):
        return self.function(*args)
