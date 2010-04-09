
def default_reproduction(parameter_constraint_list, 
                         crossover_rate=DEFAULT_CR, 
                         mutation_rate=DEFAULT_MR,
                         perturbation_rate=DEFAULT_PR,
                         num_points=DEFAULT_NP):
    """
    Inputs:
        parameter_constraint_list   : A list of tuples which
                                      give bounds on parameters
      --kwargs--
        crossover_rate              : how likely the reproduction swaps
                                      gene sequences (see glossary)
        mutation_rate               : how likely any individual parameter
                                      will take on a completely random value
        purterbation_rate           : how likely any idividual parameter
                                      will slightly change.
        num_points                  : Number of values chosen between bounds
                                      for each parameter.
    Returns:
        reproduction_object
    """
    # find out if any parameters have no constraints
    for constraint in parameter_constraint_list:
        if constraint is None:
            # hand off to more flexible reproduction
            raise NotImplimentedError()
            
    allowed_parameter_values = []
    # determine the allowed parameter values
    for constraint in parameter_constraint_list:
        # figure out the mesh details
        if math.log(constraint[1]-constraint[0], 10) > 3.0:
            # if the constraints vary over more than 3 orders...
            mesh = meshes.logmesh(constraints, num_points)
        else:
            mesh = meshes.linmesh(constraints, num_points)
        allowed_parameter_values.append(mesh)    

    # return basic constrained reproduction
    return reproduction_objects.DiscreteStandard(allowed_parameter_values, 
                                                 crossover_rate,
                                                 mutation_rate,
                                                 perturbation_rate)

    
