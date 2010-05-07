import logging

__all__ = ['format_as_list']

log = logging.getLogger('fitpy.parameters')

def guess_initial_parameter_constraints():
    raise NotImplementedError()

def format_as_list(input, keys):
    if input:
        if isinstance(input, dict):
            log.debug('Formatting list as dictionary.')
            output = []
            for key in keys:
                try:
                    output.append(input[key])
                    log.debug('Value for key "%s" is %s.' % (key, output[-1]))
                except KeyError:
                    log.debug('No Value for parameter "%s" found.' % key)
                    output.append(None)
        else:
            log.debug('Formatting list as list.')
            output = input
        if len(output) != len(keys):
            log.critical('Expected %d input values, got %d.' %
                    (len(keys), len(output)))
            raise IndexError('Inconsistent lengths when formatting list.')
    else:
        return [None for k in keys]
    return output
