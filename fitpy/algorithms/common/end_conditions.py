import datetime

from fitpy.utils import logutils
logger = logutils.getLogger(__file__)

__all__ = ['MaxIterations', 'MaxRuntime', 'StoppedImproving', 'FitTolerance']

class EndCondition(object):
    def __call__(self, variables):
        check_result = self.check(variables)
        if check_result:
            logger.info('Met end condition: %s' % self )
        return check_result

    def check(self, variables):
        raise NotImplementedError()

    def __str__(self):
        return "Undifferentiated EndCondition"


class Counter(EndCondition):
    def __init__(self, max_count):
        self.max_count = max_count
        self.remaining = max_count

    def reset(self):
        self.remaining = self.max_count

    def __str__(self):
        return "%s: %d" %(type(self).__name__, self.max_count)


class MaxIterations(Counter):
    def check(self, variables):
        self.remaining -= 1
        return 0 >= self.remaining


class MaxEvaluations(Counter):
    def check(self, variables):
        return variables['num_evaluations'] >= self.max_count


class FitTolerance(EndCondition):
    '''
    End condition to specify a minimum residual or cost function.
    '''
    def __init__(self, tolerance):
        self.tolerance = tolerance

    def check(self, variables):
        return  variables['best_fitness'] < self.tolerance

    def reset(self):
        pass

    def __str__(self):
        return "%s: %f" % (type(self).__name__, self.tolerance)
    

class MaxRuntime(EndCondition):
    """
    End condition to specify a maximum amount of time to run (approximate).
    """
    def __init__(self, run_duration):
        """
        run_duration is the amount of time to run the simulation.
            Must be either a datetime.timedelta() object, or a number of
            seconds.
        """
        try:
            self.run_duration = datetime.timedelta(seconds=run_duration)
        except TypeError:
            self.run_duration = run_duration

        self.finish_time  = datetime.datetime.now() + run_duration

    def check(self, variables):
        return self.finish_time < datetime.datetime.now()

    def reset(self):
        self.finish_time  = datetime.datetime.now() + self.run_duration

    def __str__(self):
        return "%s: %s" % (type(self).__name__, str(self.run_duration))


class StoppedImproving(EndCondition):
    """
        Specify a maximum number of generations to go without improving
    the most fit individual.
    """
    def __init__(self, static_generations):
        self.static_generations = static_generations
        self.unchanged = 0
        self.last_fitness = None
        self.finished = False

    def check(self, variables):
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

    def __str__(self):
        return "%s: allowed static generations = %d" % (type(self).__name__, 
                                                        self.static_generations)
