import bisect

from itertools import izip
from collections import namedtuple

from .settings import *

MORankingProperties = namedtuple('MORankingProperties',
                                 'trails trumps age cost parameters')
SORankingProperties = namedtuple('SORankingProperties',
                                 'cost parameters')

class SingleObjectiveParameterQueue(list):
    def __init__(self, max_length=DEFAULT_MAX_RANKING_LENGTH, **kwargs):
        self.max_length = max_length

    def append(self, item):
        raise NotImplementedError(
            "Cannot append elements to this container.  Try 'add' instead.")

    def add(self, new_parameters, new_cost):
        try:
            if new_cost < self[-1].cost:
                pass
        except IndexError:
            pass

        bisect.insort_left(self, SORankingProperties(new_cost, new_parameters))

        if(len(self) > self.max_length):
            self.pop()

class MultiObjectiveParameterQueue(list):
    '''
        A ranked list of parameter batches, ranked based on their evaluation 
    cost.  If the cost function returns multiple values then multi-objective
    ranking is used.  Parameter batches are ranked as they are added.
    '''
    def __init__(self, max_length=DEFAULT_MAX_RANKING_LENGTH, **kwargs):
        self._current_age = 0
        self.max_length
        
    def append(self, item):
        raise NotImplementedError(
            "Cannot append elements to this container.  Try 'add' instead.")

    def add(self, new_parameters, new_cost):
        try:
            if trails(new_cost, self[-1].cost):
                return
        except IndexError:
            pass

        num_trumps = 0
        num_trails = 0
        for i, rp in enumerate(self):
            if trumps(new_cost, rp.cost):
                num_trumps += 1
                rp.trails += 1
            elif trails(new_cost, rp.cost):
                num_trails += 1
                rp.trumps += 1

        self._current_age -= 1
        new_rp = MORankingProperties(num_trails, num_trumps, self._current_age,
                                     new_cost, new_parameters)
        bisect.insort_left(self, new_rp)

        if(len(self) > self.max_length):
            self.pop()
        
    def pop(self):
        dead_rp = list.pop(self)
        running_trails = 0
        for i, good_rp in enumerate(self):
            if trumps(good_rp.cost, dead_rp.cost):
                running_trails += 1
                good_rp.trumps -= 1

            if running_trails == dead_rp.trails:
                break

        return dead_rp


def trumps(cost1, cost2):
    return all(f1 > f2 for f1, f2 in izip(cost1, cost2))

def trails(cost1, cost2):
    return all(f1 < f2 for f1, f2 in izip(cost1, cost2))
