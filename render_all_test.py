#!/usr/bin/env python

import unittest
from render_all import *

class Get_Commands_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_zero_scenes_should_result_in_zero_commands(self):
		result = get_commands([], "", 0)

		self.assertEqual(len(result), 0)

	def test_one_scene_should_result_in_one_command(self):
		result = get_commands([""], "", 0)

		self.assertEqual(len(result), 1)


if __name__ == "__main__":
	unittest.main()
