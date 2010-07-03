from .functions import schaffer_f6

cost_function = schaffer_f6.schaffer_f6

kwargs = {'parameter_constraints': [[-10.0, 10.0], [-10.0, 10.0]],
          'target_cost': 0.001,
          'max_evaluations': None,
          'num_points':10000}
