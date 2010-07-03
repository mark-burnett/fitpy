import os

from . import common

# Generate list of legal algorithm names.
_ignored_strings = ['.', 'common']
_dirname = os.path.dirname(__file__)
algorithm_names = []
for file in os.listdir(_dirname):
    if not any(s in file for s in _ignored_strings):
        algorithm_names.append(file)

del _ignored_strings
del _dirname
del os
