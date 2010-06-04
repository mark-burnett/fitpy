import bisect

from itertools import izip
from collections import namedtuple

from .settings import *

MORankingProperties = namedtuple('MORankingProperties',
                                 'trails trumps age fitness parameters')
SORankingProperties = namedtuple('SORankingProperties',
                                 'fitness parameters')

class SingleObjectiveParameterQueue(list):
    def __init__(self, max_length=DEFAULT_MAX_RANKING_LENGTH, **kwargs):
        self.max_length = max_length

    def append(self, item):
        raise NotImplementedError(
            "Cannot append elements to this container.  Try 'add' instead.")

    def add(self, new_parameters, new_fitness):
        try:
            if new_fitness < self[-1].fitness:
                pass
        except IndexError:
            pass

        bisect.insort_left(self, SORankingProperties(new_fitness, new_parameters))

        if(len(self) > self.max_length):
            self.pop()

class MultiObjectiveParameterQueue(list):
    '''
        A ranked list of parameter batches, ranked based on their evaluation 
    fitnesses.  If the fitness function returns multiple values then 
    multi-objective ranking is used.  Parameter batches are ranked as they 
    are added.
    '''
    def __init__(self, max_length=DEFAULT_MAX_RANKING_LENGTH, **kwargs):
        self._current_age = 0
        self.max_length
        
    def append(self, item):
        raise NotImplementedError(
            "Cannot append elements to this container.  Try 'add' instead.")

    def add(self, new_parameters, new_fitness):
        try:
            if trails(new_fitness, self[-1].fitness):
                return
        except IndexError:
            pass

        num_trumps = 0
        num_trails = 0
        for i, rp in enumerate(self):
            if trumps(new_fitness, rp.fitness):
                num_trumps += 1
                rp.trails += 1
            elif trails(new_fitness, rp.fitness):
                num_trails += 1
                rp.trumps += 1

        self._current_age -= 1
        new_rp = MORankingProperties(num_trails, num_trumps, self._current_age,
                                     new_fitness, new_parameters)
        bisect.insort_left(self, new_rp)

        if(len(self) > self.max_length):
            self.pop()
        
    def pop(self):
        dead_rp = list.pop(self)
        running_trails = 0
        for i, good_rp in enumerate(self):
            if trumps(good_rp.fitness, dead_rp.fitness):
                running_trails += 1
                good_rp.trumps -= 1

            if running_trails == dead_rp.trails:
                break

        return dead_rp


def trumps(fitness1, fitness2):
    return all(f1 > f2 for f1, f2 in izip(fitness1, fitness2))

def trails(fitness1, fitness2):
    return all(f1 < f2 for f1, f2 in izip(fitness1, fitness2))
