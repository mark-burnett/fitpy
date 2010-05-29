import datetime
import time
import unittest

from fitpy.algorithms.common import end_conditions

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

class TestTimer(unittest.TestCase):
    def testNormal(self):
        delta = datetime.timedelta(milliseconds=5)

        # Offset the count by one, or miss due to loop run time.
        count = 1
        t = end_conditions.Timer(delta)
        while not t(None):
            time.sleep(1e-3)
            if not t(None):
                count += 1
        self.assertEqual(5, count)

        count = 1
        t.reset()
        while not t(None):
            time.sleep(1e-3)
            if not t(None):
                count += 1
        self.assertEqual(5, count)

class TestStoppedImproving(unittest.TestCase):
    def testIncreasing(self):
        increasing = end_conditions.StoppedImproving(3)
        values = [1, 2, 3, 3, 3, 4, 3, 5, 5, 5, 5, 6, 6, 7, 8, 9]

        for i, v in enumerate(values):
            result = increasing(v)
            if 10 <= i:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

        increasing.reset()
        for i, v in enumerate(values):
            result = increasing(v)
            if 10 <= i:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def testDecreasing(self):
        decreasing = end_conditions.StoppedImproving(3)
        values = [9, 9, 9, 8, 7, 7, 6, 6, 6, 6, 5, 4, 3, 2, 2]

        for i, v in enumerate(values):
            result = decreasing(v)
            if 9 <= i:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

        decreasing.reset()
        for i, v in enumerate(values):
            result = decreasing(v)
            if 9 <= i:
                self.assertTrue(result)
            else:
                self.assertFalse(result)


if '__main__' == __name__:
    unittest.main()
