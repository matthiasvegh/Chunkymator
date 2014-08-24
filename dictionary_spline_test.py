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


	def test_values_of_controls_should_match_in_two_parameters(self):
		vector1 = [1, 2, 3, 4]
		vector2 = [2, 3, 4, 5]
		times = [1, 2, 3, 4]

		matrix = [vector1, vector2]

		v = VectorSpline(matrix, times)
		results = []
		for i in times:
			results.append(v(i))

		for i in range(4):
			self.assertAlmostEqual(results[i][0], vector1[i])
			self.assertAlmostEqual(results[i][1], vector2[i])

	def test_strings_should_not_be_interpolated(self):
		vector = ["a", "b", "c", "d"]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = []
		for i in times:
			results.append(v(i))

		for result in results:
			self.assertEqual(result, ["a"])

	def test_tuples_should_be_interpolated_piecewise(self):
		vector = [(1, 10), (2, 20), (3, 30), (4, 40)]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = []
		for i in times:
			results.append(v(i))

		for i in range(4):
			self.assertAlmostEqual(results[i][0][0], vector[i][0])

if __name__ == "__main__":
	unittest.main()
