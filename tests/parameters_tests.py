import unittest
import logging

from fitpy import parameters

class TestFormatAsList(unittest.TestCase):
    def test_from_dictionary(self):
        parameter_names = ['a', 'd', 'z']
        dict_param_constraints = {'a':(0, 1), 'z':(-1, 2), 'extra':123}
        self.assertEqual([(0,1), None, (-1,2)],
                parameters.format_as_list(
                    dict_param_constraints, parameter_names))

    def test_from_list(self):
        parameter_names = ['a', 'd', 'z']
        list_param_constraints = [(0,1), None, (-1,2)]
        self.assertEqual([(0,1), None, (-1,2)],
                parameters.format_as_list(
                    list_param_constraints, parameter_names))

        bad_param_constraints = [1, 2, 3, 4]
        self.assertRaises(IndexError,
                parameters.format_as_list,
                    bad_param_constraints, parameter_names)

        bad_param_constraints2 = [1, 2]
        self.assertRaises(IndexError,
                parameters.format_as_list,
                    bad_param_constraints2, parameter_names)

if '__main__' == __name__:
    log = logging.getLogger('fitpy')
    log.setLevel(1000)
    unittest.main()
