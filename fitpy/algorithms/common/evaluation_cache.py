try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        raise ImportError("Couldn't find an ordered dictionary class to import, either install ordereddict from pypi or upgrade to Python 2.7 or newer.")


class EvaluationCache(OrderedDict):
    """
        Base class to keep track of all fitness function evaluations and
    the parameter set used.
    """
    def get_fitness(self, i):
        return self[i]
    
    @property
    def num_evaluations(self):
        return len(self)
