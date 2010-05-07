import random

def choose_two(sequence, select_function):
    """
    Picks 2 unique items from the sequence.
    """
    p1 = select_function(sequence)
    p2 = p1
    while p1 == p2:
        p2 = select_function(sequence)
    return p1, p2

def weighted_choice(sequence, width=None):
    """
        Choose a random element from sequence, weighted toward the
    front of the list.
    """
    if not width:
        width = float(len(sequence))/2
    j = len(sequence)
    while j >= len(sequence):
        j = abs(int(random.normalvariate(0, width)))
    return sequence[j]
