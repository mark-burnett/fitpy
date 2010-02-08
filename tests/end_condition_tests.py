from fitpy import end_conditions
import unittest

class TestCounter(unittest.TestCase):
    def testNormal(self):
        c = end_conditions.Counter(50)
        self.assertFalse(any(c(None) for i in xrange(49)))
        self.assertTrue(c(None))
        self.assertTrue(c(None))
        c.reset()
        self.assertFalse(any(c(None) for i in xrange(49)))
        self.assertTrue(c(None))
        self.assertTrue(c(None))
        c.reset()
        self.assertFalse(any(c(None) for i in xrange(20)))
        c.reset()
        self.assertFalse(any(c(None) for i in xrange(49)))
        self.assertTrue(c(None))
        self.assertTrue(c(None))

if '__main__' == __name__:
    unittest.main()
