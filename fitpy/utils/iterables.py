def isiterable(obj):
    return hasattr(obj, '__iter__')

def get_two(iterable):
    iterator = iter(iterable)
    first = iterator.next()
    for second in iterator:
        yield (first, second)
        first = second
