#!/usr/bin/env python

import itertools

import baker

from fitpy.utils import iterables
from fitpy.optimize import optimize

import benchmarks as bm
import fitpy.algorithms.algorithm_names

def decode_names(names, module):
    iterable_names = iterables.make_iterable(names)
    return [getattr(module, name) for name in iterable_names]

def run_benchmarks(algorithm_names, benchmarks):
    results = []
    for algorithm_name, benchmark in itertools.product(algorithm_names,
                                                       benchmarks):
        full_results = optimize(benchmark.cost_function, 
                                algorithm_name=algorithm_name, 
                                **benchmark.kwargs)
        useful_results = {'num_evaluations': len(full_results['evaluation_cache']),
                          'cost': full_results['best_cost']}
        results.append(useful_results)

    return results

def display_benchmark_results(results):
    for result in results:
        print result['num_evaluations']
        print result['cost']
#        print len(result['evaluation_cache'])
#        print result['best_parameters']
#        print result['best_cost']

@baker.command
def algorithm(algorithm_name, benchmark_names=None, num_runs=1):
    """
    :param algorithm_name: Name of the algorithm to benchmark.
    :param benchmarks: Which benchmarks to run (default = all).
    :param num_runs: How many times to perform each benchmark.
    """
    if benchmark_names is None:
        # Get list of all benchmarks
        benchmarks = bm.all_benchmarks
    else:
        benchmarks = decode_names(benchmark_names, bm)

    results = run_benchmarks([algorithm_name], benchmarks)

    display_benchmark_results(results)

@baker.command
def benchmark(benchmark_name, algorithms=None, num_runs=1):
    print 'benchmark', benchmark_name

@baker.command(default=True)
def all(num_runs=50):
    benchmarks = bm.all_benchmarks
    algorithm_names = fitpy.algorithms.algorithm_names.algorithm_names

    results = run_benchmarks(algorithm_names, benchmarks)

    display_benchmark_results(results)

baker.run()
