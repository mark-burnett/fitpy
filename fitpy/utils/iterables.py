def isiterable(obj):
    return hasattr(obj, '__iter__')

def make_iterable(obj, iter_type=list):
    if isiterable(obj):
        return obj
    return iter_type([obj])

def get_two(iterable):
    iterator = iter(iterable)
    first = iterator.next()
    for second in iterator:
        yield (first, second)
        first = second
