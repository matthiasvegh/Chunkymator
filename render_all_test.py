import unittest
from render_all import *

class Get_Commands_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_zero_scenes_should_result_in_zero_commands(self):
		result = get_commands([], "", 0)

		self.assertEqual(len(result), 0)

if __name__ == "__main__":
	unittest.main()
