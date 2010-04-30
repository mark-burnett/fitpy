import math

def linmesh(min, max, num_points):
    '''
    Create a linear mesh of points between and including
       the min and max values passed.
    '''
    dx = (max-min)/float(num_points)
    return [min+dx*i for i in range(num_points)]
