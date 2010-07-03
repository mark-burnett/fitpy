#!/usr/bin/env python

import itertools

import numpy

import baker

from fitpy.utils import iterables
from fitpy.optimize import optimize

import benchmarks as bm
import fitpy.algorithms.algorithm_names

def decode_names(names, module):
    iterable_names = iterables.make_iterable(names)
    return [getattr(module, name) for name in iterable_names]

def run_benchmark(algorithm_name, benchmark, num_runs):
    evaluation_counts = []
    costs = []
    for i in xrange(num_runs):
        full_results = optimize(benchmark.cost_function, 
                                algorithm_name=algorithm_name, 
                                **benchmark.kwargs)
        evaluation_counts.append(len(full_results['evaluation_cache']))
        costs.append(full_results['best_cost'])

    return {'num_evaluations_average': numpy.average(evaluation_counts),
            'num_evaluations_std': numpy.std(evaluation_counts),
            'cost_average': numpy.average(costs),
            'cost_std': numpy.std(costs)}

def run_benchmarks(algorithm_names, benchmarks, num_runs):
    results = []
    for algorithm_name, benchmark in itertools.product(algorithm_names,
                                                       benchmarks):
        results.append(run_benchmark(algorithm_name, benchmark, num_runs))

    return results

def display_benchmark_results(results):
    for result in results:
        print result['num_evaluations_average'], result['num_evaluations_std']
        print result['cost_average'], result['cost_std']
#        print len(result['evaluation_cache'])
#        print result['best_parameters']
#        print result['best_cost']

#@baker.command
#def algorithm(algorithm_name, benchmark_names=None, num_runs=1):
#    """
#    :param algorithm_name: Name of the algorithm to benchmark.
#    :param benchmarks: Which benchmarks to run (default = all).
#    :param num_runs: How many times to perform each benchmark.
#    """
#    if benchmark_names is None:
#        # Get list of all benchmarks
#        benchmarks = bm.all_benchmarks
#    else:
#        benchmarks = decode_names(benchmark_names, bm)
#
#    results = run_benchmarks([algorithm_name], benchmarks)
#
#    display_benchmark_results(results)
#
#@baker.command
#def benchmark(benchmark_name, algorithms=None, num_runs=1):
#    print 'benchmark', benchmark_name

@baker.command(default=True)
def all(num_runs=50):
    benchmarks = bm.all_benchmarks
    algorithm_names = fitpy.algorithms.algorithm_names.algorithm_names

    results = run_benchmarks(algorithm_names, benchmarks, num_runs)

    display_benchmark_results(results)

baker.run()
