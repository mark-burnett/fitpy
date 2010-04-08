from itertools import izip

__all__ = ['chi_squared', 'residual_functions']

def chi_squared(x_values, y_values, y_stds, y_calculated):
    if y_stds:
        return sum([((y1-y2)/ys)**2
                    for y1, y2, ys in izip(y_values, y_calculated, y_stds)])
    else:
        return sum([(y1-y2)**2 for y1, y2 in izip(y_values, y_calculated)])

residual_functions = {'chi_squared': chi_squared}
