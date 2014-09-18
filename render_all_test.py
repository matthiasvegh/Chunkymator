#!/usr/bin/env python

import unittest
import mock
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

class Get_Command_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_first_two_parameters_should_always_be_java_and_jar(self):
		result = get_command("", "", 0)

		self.assertEqual(result[0], "java")
		self.assertEqual(result[1], "-jar")

	def test_third_parameter_should_be_path_to_chunky(self):
		result = get_command("", "Chunky", 0)

		self.assertEqual(result[2], "Chunky")

	def test_fourth_and_fifth_parameter_should_be_render_and_scene(self):
		result = get_command("foo", "", 0)

		self.assertEqual(result[3], "-render")
		self.assertEqual(result[4], "foo")

	def test_sixth_and_seventh_parameter_should_be_target_and_value(self):
		result = get_command("", "", 5)

		self.assertEqual(result[5], "-target")
		self.assertEqual(result[6], 5)

class Render_All_Main_Test(unittest.TestCase):

	def setUp(self):
		pass



if __name__ == "__main__":
	unittest.main()
