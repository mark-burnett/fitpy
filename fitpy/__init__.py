import logging

from residual_fit import residual_fit

__all__ = ['residual_fit']

log = logging.getLogger('fitpy')
log.setLevel(logging.WARNING)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

handler.setFormatter(logging.Formatter('%(levelname)s %(name)s: %(message)s'))

log.addHandler(handler)
