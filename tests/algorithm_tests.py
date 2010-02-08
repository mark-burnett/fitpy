import unittest
from mock import Mock

from fitpy import algorithm
from fitpy import end_conditions

class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        # Evaluation callable
        self.eval_cache = set()
        def evaluate(chromosomes):
            results = []
            for chromosome in chromosomes:
                # This will catch double evaluations
                self.assertFalse(chromosome in self.eval_cache)
                self.eval_cache.add(chromosome)
                results.append(Mock())
            return results

        # Rank callable
        def rank(pop, cache):
            return sorted(pop, key=cache.__getitem__)

        # Reproduction object
        def reproduce(ranked_pop, cache):
            return [Mock() for p in ranked_pop]

        def random_population(pop_size):
            return [Mock() for i in xrange(pop_size)]

        reproduce.random_population = random_population

        # End conditions
        self.iter_count = 10
        end = [Mock(), end_conditions.Counter(self.iter_count), Mock()]
        end[0].return_value = False
        end[2].return_value = False

        # Build GA object
        self.GA = algorithm.GeneticAlgorithm(evaluate, rank, reproduce, end)

    def TotalEvaluationsTest(self):
        self.assertEqual(self.init_pop_size
                            + (self.iter_count - 1) * self.pop_size,
                        len(self.eval_cache))

    def EndConditionCallsTest(self):
        self.assertEqual(self.GA.end[0].call_count, self.iter_count)
        self.assertEqual(self.GA.end[2].call_count, self.iter_count - 1)

    def BestResultTest(self):
        best = self.result[0]
        best_fitness = self.result[1]
        cache = self.GA.cache
        self.assertEqual(best_fitness, cache[best])
        self.assertTrue(best_fitness <= f for f in cache.keys())

    def runTest(self):
        # Run fit
        self.init_pop_size = 2000
        self.pop_size      = 500
        self.elite_size    = 10
        self.result = self.GA.fit(self.pop_size, self.init_pop_size,
                                  self.elite_size)

        self.TotalEvaluationsTest()
        self.EndConditionCallsTest()
        self.BestResultTest()

if '__main__' == __name__:
    unittest.main()
