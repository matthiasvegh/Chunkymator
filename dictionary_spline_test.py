import unittest
from dictionary_spline import *

class VectorSplineTest(unittest.TestCase):

	def setUp(self):
		pass

	def test_values_of_controls_should_match_in_one_parameter(self):
		vector = [1, 2, 3, 4]
		times = [1, 2, 3, 4]

		matrix = [vector]

		v = VectorSpline(matrix, times)
		results = []
		for i in times:
			results.append(v(i))

		for i in range(4):
			self.assertAlmostEqual(results[i][0], vector[i])


if __name__ == "__main__":
	unittest.main()
