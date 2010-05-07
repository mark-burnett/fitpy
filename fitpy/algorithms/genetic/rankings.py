def general(generation, fitnesses, maximize=False):
    try:
        iter(fitnesses[0])
        return multi_objective(generation, fitnesses, maximize)
    except TypeError:
        return single_objective(generation, fitnesses, maximize)

def multi_objective(generation, fitnesses, maximize):
    """
        Ranks population using fitnesses from cache based on
    how many others in population dominate an individual.  Secondary
    rank based on how many in the population it dominates.
    """
    num_objectives = len(fitnesses[0])
    if maximize:
        compare = lambda a, b: a > b
    else:
        compare = lambda a, b: a < b

    bottom_counts = {}
    top_counts = {}
    for i1, individual in enumerate(generation):
        fitness1 = fitnesses[i1]
        bottom = 0
        top = 0
        for i2 in xrange(len(generation)):
            if i1 != i2:
                fitness2 = fitnesses[i2]
                if all(compare(f2, f1) for f1, f2 in zip(fitness1, fitness2)):
                    bottom += 1
                if all(compare(f1, f2) for f1, f2 in zip(fitness1, fitness2)):
                    top += 1

        bottom_counts[individual] = bottom
        top_counts[individual] = top

    # Sort and return
    gen_fitnesses = zip(generation, fitnesses)
    tiebreak_sorted = sorted(gen_fitnesses,
                             key=lambda x: top_counts[x[0]],
                             reverse=True)
    ranked_gen, ranked_fitnesses = zip(*sorted(tiebreak_sorted,
                                       key=lambda x: bottom_counts[x[0]]))
    return list(ranked_gen), list(ranked_fitnesses)

def single_objective(generation, fitnesses, maximize):
    """
    Uses the multi_objective ranking function to provide a
    single objective ranking function.
    """
    crazy_fitnesses = [(f,) for f in fitnesses]
    ranked_gen, ranked_crazy_fitnesses = multi_objective(generation,
                                            crazy_fitnesses, maximize)
    return ranked_gen, [f[0] for f in ranked_crazy_fitnesses]
