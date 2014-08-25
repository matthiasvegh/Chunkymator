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
		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0], vector[i])


	def test_values_of_controls_should_match_in_two_parameters(self):
		vector1 = [1, 2, 3, 4]
		vector2 = [2, 3, 4, 5]
		times = [1, 2, 3, 4]

		matrix = [vector1, vector2]

		v = VectorSpline(matrix, times)
		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0], vector1[i])
			self.assertAlmostEqual(results[i][1], vector2[i])

	def test_strings_should_not_be_interpolated(self):
		vector = ["a", "b", "c", "d"]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for result in results:
			self.assertEqual(result, ["a"])

	def test_tuples_should_be_interpolated_piecewise(self):
		vector = [(1, 10), (2, 20), (3, 30), (4, 40)]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0][0], vector[i][0])
			self.assertAlmostEqual(results[i][0][1], vector[i][1])

	def test_tuples_should_be_interpolated_piecewise_even_if_other_params_are_present(self):
		vector1 = [(1, 10), (2, 20), (3, 30), (4, 40)]
		vector2 = [100, 200, 300, 400]
		times = [1, 2, 3, 4]
		matrix = [vector1, vector2]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0][0], vector1[i][0])
			self.assertAlmostEqual(results[i][0][1], vector1[i][1])
			self.assertAlmostEqual(results[i][1], vector2[i])

	def test_recursive_tuples_should_be_recursively_interpolated(self):
		vector = [((1, 10), 100), ((2, 20), 200), ((3, 30), 300), ((4, 40), 400)]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0][0][0], vector[i][0][0])
			self.assertAlmostEqual(results[i][0][0][1], vector[i][0][1])
			self.assertAlmostEqual(results[i][0][1], vector[i][1])

	def test_scalar_dictionaries_should_be_interpolated_regularly(self):
		vector = [{'x':1}, {'x':2}, {'x':3}, {'x':4}]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0]['x'], vector[i]['x'])

	def test_non_scalar_dictionaries_should_be_interpolated_correctly(self):
		vector = [
				{'x':1, 'y':10, 'z':100},
				{'x':2, 'y':20, 'z':200},
				{'x':3, 'y':30, 'z':300},
				{'x':4, 'y':40, 'z':400}]
		times = [1, 2, 3, 4]
		matrix = [vector]
		v = VectorSpline(matrix, times)

		results = [v(i) for i in times]

		for i in range(4):
			self.assertAlmostEqual(results[i][0]['x'], vector[i]['x'])
			self.assertAlmostEqual(results[i][0]['y'], vector[i]['y'])
			self.assertAlmostEqual(results[i][0]['z'], vector[i]['z'])

if __name__ == "__main__":
	unittest.main()
