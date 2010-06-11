import itertools

from fitpy.utils import iterables

def count_crossings(yvalues1, yvalues2):
    """
    Counts the number of times these function evaluations cross each other.
    Cases where the two come together to identical values, or separate from
    identical values do not count as crossing.

    Thus two identical sets of values cross each other zero times.
    """
    num_crossings = 0
    for y1, y2 in itertools.izip(iterables.get_two(yvalues1),
                                 iterables.get_two(yvalues2)):
        dlow  = y1[0] - y2[0]
        dhigh = y1[1] - y2[1]
        if dlow * dhigh < 0:
            num_crossings += 1

    return num_crossings
