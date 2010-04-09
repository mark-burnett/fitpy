def multi_objective(population, cache):
    """
        Ranks population using fitnesses from cache based on
    how many others in population dominate an individual.  Secondary
    rank based on how many in the population it dominates.
    """
    all_fitnesses = [cache[individual] for individual in population]
    num_objectives = len(all_fitnesses[0])

    bottom_counts = {}
    top_counts = {}
    for i1, individual in enumerate(population):
        fitness1 = all_fitnesses[i1]
        bottom = 0
        top = 0
        for i2 in xrange(len(population)):
            if i1 != i2:
                fitness2 = all_fitnesses[i2]
                if all(f1 < f2 for f1, f2 in zip(fitness1, fitness2)):
                    bottom += 1
                if all(f1 > f2 for f1, f2 in zip(fitness1, fitness2)):
                    top += 1
        bottom_counts[individual] = bottom
        top_counts[individual] = top

    # Sort and return
    tiebreak_sorted = sorted(population, key=top_counts.__getitem__,
                             reverse=True)
    return sorted(tiebreak_sorted, key=bottom_counts.__getitem__)
