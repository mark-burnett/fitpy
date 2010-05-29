from itertools import izip
from collections import namedtupple

class ParameterQueue(object):
    '''
        A ranked list of parameter batches, ranked based on their evaluation 
    fitnesses.  If the fitness function returns multiple values then 
    multi-objective ranking is used.  Parameter batches are ranked as they 
    are added.
    '''
    def __init__(self, max_length=DEFAULT_MAX_RANKING_LENGTH):
        self._parameter_batches = []
        self._fitnesses = []
        self._scores = []
        self._trumps = []
        self._trails = []
        self.max_length
        
    def determine_kind(self, fitness):
        try:
            iter(fitness)
            self.add = self.multi_objective_add 
        except TypeError:
            self.add = self.single_objective_add

    def add(self, parameter_batch, fitness):
        self.determine_kind(fitness)
        self.add(parameter_batch, fitness)


    def multi_objective_add(self, new_parameter_batch, new_fitness):
        if trumps(new_fitness, self._fitnesses[-1]):
            return

        trumps = 0
        trails = 0
        for i, old_fitness in enumerate(self._fitnesses):
            if trumps(new_fitness, old_fitness):
                trumps += 1
                self._trails[i] += 1 
                self.calculate_score_for_index(i)
            elif trumps(old_fitness, new_fitness):
                trails += 1
                self._trumps[i] += 1
                self.calculate_score_for_index(i)

        new_score = calculate_score(trumps, trails, self.max_length)
        new_position = bisect.bisect_left(self._scores, new_score)
        self._parameter_batches.insert(new_position, new_parameter_batch)
        self._fitnesses.insert(new_position, new_fitness)
        self._scores.insert(new_position, new_score)
        self._trumps.insert(new_position, trumps)
        self._trails.insert(new_position, trails)

        if(len(self) >= self.max_length):
            dead_parameter_batch = self._parameter_batches.pop()
            dead_fitness = self._fitnesses.pop()
            self._scores.pop()
            self._trumps.pop()
            dead_trails = self._trails.pop()
        
        running_trails = 0
        for i, kept_fitness in enumerate(self._fitnesses):
            if trumps(kept_fitness, dead_fitness):
                running_trails += 1
                self._trumps[i] -= 1
                self.calculate_score_for_index(i)

            if running_trails == dead_trails:
                break

    def __getitem__(self, index):
        return self._parameter_batches[index]
    
    def __getslice__(self, begin, end):
        return self._parameter_batches.__getslice__(begin, end)

    def __len__(self):
        return len(self._parameter_batches)

    def calculate_score_for_index(self, index):
        self._score[index] = calculate_score(self._trumps[index],
                                             self._trails[index],
                                             self.max_length)

    def __iter__(self):
        return iter(self._parameter_batches)


def trumps(fitness1, fitness2):
    return all(f2 < f1 for f1, f2 in izip(fitness1, fitness2))

def calculate_score(trails, trumps, max_length):
    return -max_length*trails + trumps
