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

    def test_sixth_and_seventh_parameter_should_be_scene_dir_and_path(self):
        result = render_all.get_command("/foo", "", 5)

        self.assertEqual(result[5], "-scene-dir")
        self.assertEqual(result[6], "/")

    def test_eigth_and_ninth_parameter_should_be_target_and_value(self):
        result = render_all.get_command("", "", 5)

        self.assertEqual(result[7], "-target")
        self.assertEqual(result[8], '5')


class Render_All_Main_Test(unittest.TestCase):

    def setUp(self):
        self.gc = render_all.get_commands
        self.rc = render_all.run_command

    def tearDown(self):
        render_all.get_commands = self.gc
        render_all.run_command = self.rc

    def test_if_arguments_are_okay_get_commands_should_be_called(self):
        sys.argv = ["thisBinary", "-c", "foo"]
        render_all.get_commands = mock.MagicMock(name='get_commands')
        render_all.main()
        render_all.get_commands.assert_called_once_with([], "foo", 1)

    def test_if_chunky_argument_missing__get_commands_shouldnt_be_called(self):
        sys.argv = ["thisBinary"]
        render_all.get_commands = mock.MagicMock(name='get_commands')
        render_all.main()
        self.assertNotEqual(render_all.get_commands.called, True)

    def test_zero_scenes_shoule_invoke_no_commands(self):
        sys.argv = ["thisBinary", "-c", "foo"]
        render_all.run_command = mock.MagicMock(name='run_command')
        render_all.main()
        self.assertNotEqual(render_all.run_command.called, True)

    def test_one_scene_should_invoke_one_command(self):
        sys.argv = ["thisBinary", "-c", "foo", "scene1"]
        render_all.run_command = mock.MagicMock(name='run_command')
        render_all.main()
        self.assertEqual(len(render_all.run_command.call_args_list), 1)

    def test_two_scenes_should_invoke_two_commands(self):
        sys.argv = ["thisBinary", "-c", "foo", "scene1", "scene2"]
        render_all.run_command = mock.MagicMock(name='run_command')
        render_all.main()
        self.assertEqual(len(render_all.run_command.call_args_list), 2)

if __name__ == "__main__":
    unittest.main()
