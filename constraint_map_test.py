#!/usr/bin/env python

import unittest
from constraint_map import *

class BasicTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_construct(self):
        ConstraintMap(['a'], [lambda x: x])

if __name__ == "__main__":
    unittest.main()
