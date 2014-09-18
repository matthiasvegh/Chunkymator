#!/usr/bin/env python

import sys
import unittest
import mock
import render_all

class Get_Commands_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_zero_scenes_should_result_in_zero_commands(self):
		result = render_all.get_commands([], "", 0)

		self.assertEqual(len(result), 0)

	def test_one_scene_should_result_in_one_command(self):
		result = render_all.get_commands([""], "", 0)

		self.assertEqual(len(result), 1)

class Get_Command_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_first_two_parameters_should_always_be_java_and_jar(self):
		result = render_all.get_command("", "", 0)

		self.assertEqual(result[0], "java")
		self.assertEqual(result[1], "-jar")

	def test_third_parameter_should_be_path_to_chunky(self):
		result = render_all.get_command("", "Chunky", 0)

		self.assertEqual(result[2], "Chunky")

	def test_fourth_and_fifth_parameter_should_be_render_and_scene(self):
		result = render_all.get_command("foo", "", 0)

		self.assertEqual(result[3], "-render")
		self.assertEqual(result[4], "foo")

	def test_sixth_and_seventh_parameter_should_be_target_and_value(self):
		result = render_all.get_command("", "", 5)

		self.assertEqual(result[5], "-target")
		self.assertEqual(result[6], 5)

class Render_All_Main_Test(unittest.TestCase):

	def setUp(self):
		pass

	def test_if_arguments_are_okay_get_commands_should_be_called(self):
		sys.argv = ["thisBinary", "-c", "foo"]
		render_all.get_commands = mock.MagicMock(name='get_commands')
		render_all.main()
		render_all.get_commands.assert_called_once_with([], "foo", 1)

if __name__ == "__main__":
	unittest.main()
