import datetime

__all__ = ['Counter', 'Timer', 'Static']

class Counter(object):
    """
    End condition to specify a maximum number of generations to run.
    """
    def __init__(self, num_generations):
        self.num_left     = num_generations
        self.num_starting = num_generations
    def __call__(self, best_fitness):
        self.num_left -= 1
        return 0 >= self.num_left
    def reset(self):
        self.num_left = self.num_starting

class Timer(object):
    """
    End condition to specify a maximum amount of time to run (approximate).
    """
    def __init__(self, run_duration):
        """
        run_duration is the amount of time to run the simulation.
            Must be a datetime.timedelta() object.
        """
        self.run_duration = run_duration
        self.finish_time  = datetime.datetime.now() + run_duration
    def __call__(self, best_fitness):
        return self.finish_time < datetime.datetime.now()
    def reset(self):
        self.finish_time  = datetime.datetime.now() + self.run_duration

class Static(object):
    """
        End condition to specify a maximum numbe rof generations to go without
    improving the most fit individual.
    """
    def __init__(self, static_generations):
        self.static_generations = static_generations
        self.unchanged = 0
        self.last_fitness = None
    def __call__(self, best_fitness):
        if best_fitness == self.last_fitness:
            self.unchanged += 1
        else:
            self.unchanged = 0
            self.last_fitness = best_fitness
        if self.unchanged >= self.static_generations:
            return True
        return False
    def reset(self):
        self.last_fitness = None
        self.unchanged = 0
