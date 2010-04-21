import datetime

__all__ = ['MaxIterations', 'MaxRuntime', 'StoppedImproving']

class Counter(object):
    def __init__(self, max_count):
        self.max_count = max_count
        self.remaining = max_count
    def __call__(self, variables):
        raise NotImplementedError()
    def reset(self):
        self.remaining = self.max_count

class MaxIterations(Counter):
    def __call__(self, variables):
        self.remaining -= 1
        return 0 >= self.remaining

class MaxEvaluations(Counter):
    def __call__(self, variables):
        return variables['num_evaluations'] < self.max_count

class FitTolerance(object):
    '''
    End condition to specify a minimum residual or cost function.
    '''
    def __init__(self, tolerance):
        self.tolerance = tolerance
    def __call__(self, variables):
        return  variables['best_fitness'] < self.tolerance
    def reset(self):
        pass
    
class MaxRuntime(object):
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

    def __call__(self, variables):
        return self.finish_time < datetime.datetime.now()

    def reset(self):
        self.finish_time  = datetime.datetime.now() + self.run_duration

class StoppedImproving(object):
    """
        Specify a maximum number of generations to go without improving
    the most fit individual.
    """
    def __init__(self, static_generations):
        self.static_generations = static_generations
        self.unchanged = 0
        self.last_fitness = None
        self.finished = False

    def __call__(self, variables):
        best_fitness = variables['best_fitness']
        if not self.finished:
            if best_fitness == self.last_fitness:
                self.unchanged += 1
            else:
                self.unchanged = 0
                self.last_fitness = best_fitness

        if self.unchanged >= self.static_generations:
            self.finished = True
            return True

        return False

    def reset(self):
        self.last_fitness = None
        self.unchanged = 0
        self.finished = False
