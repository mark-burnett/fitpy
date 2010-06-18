#!/usr/bin/env python

import itertools

import baker

from fitpy.utils import iterables
import benchmarks as bm

def decode_names(names, module):
    iterable_names = iterables.make_iterable(names)
    return [getattr(module, name) for name in iterable_names]

def run_benchmarks(algorithms, benchmarks):
    results = []
    for algorithm, benchmark in itertools.product(algorithms, benchmarks):
        pass

@baker.command(default=True)
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

    results = run_benchmarks([algorithm], benchmarks)

    display_benchmark_results(results)

@baker.command
def benchmark(benchmark_name, algorithms=None, num_runs=1):
    print 'benchmark', benchmark_name

baker.run()
