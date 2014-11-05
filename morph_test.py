#!/usr/bin/env python

import unittest
import morph
import copy
import mock


class mockCVF:

    def __init__(self, x, y, z, altitude=0):
        self.x = x
        self.y = y
        self.z = z
        self.altitude = altitude

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.y and self.altitude == other.altitude

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getSunAltitude(self):
        return self.altitude

    def setSunAltitude(self, alt):
        self.altitude = alt


class GetTimes_consistency_test(unittest.TestCase):

    def setUp(self):
        tuples = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        self.mockCvfs = [mockCVF(*t) for t in tuples]

    def test_doubling_of_frame_rate_should_double_times(self):

        rate1 = 1
        rate2 = 2 * rate1

        (times1, length1) = morph.getTimes(self.mockCvfs, rate1, 1)
        (times2, length2) = morph.getTimes(self.mockCvfs, rate2, 1)

        for t1, t2 in zip(times1, times2):
            self.assertEqual(t1 * 2, t2)

    def test_doubling_of_frame_rate_should_not_influence_total_length(self):

        rate1 = 1
        rate2 = 2 * rate1

        (times1, length1) = morph.getTimes(self.mockCvfs, rate1, 1)
        (times2, length2) = morph.getTimes(self.mockCvfs, rate2, 1)

        self.assertEqual(length1, length2)

    def test_doubling_speed_should_halve_times(self):

        speed1 = 1
        speed2 = 2 * speed1

        (times1, length1) = morph.getTimes(self.mockCvfs, 1, speed1)
        (times2, length2) = morph.getTimes(self.mockCvfs, 1, speed2)

        for t1, t2 in zip(times1, times2):
            self.assertEqual(t1, t2 * 2)

    def test_appending_to_input_should_append_to_time(self):

        newCvfs = copy.deepcopy(self.mockCvfs)
        newCvfs.append(mockCVF(4, 0, 0))

        (oldTimes, oldLength) = morph.getTimes(self.mockCvfs, 1, 1)
        (newTimes, newLength) = morph.getTimes(newCvfs, 1, 1)

        for (old, new) in zip(oldTimes, newTimes):
            self.assertEqual(old, new)

        self.assertGreater(newTimes[-1], oldTimes[-1])
        self.assertEqual(len(oldTimes) + 1, len(newTimes))

    def test_triangularity_should_hold(self):

        newCvfs = [self.mockCvfs[-1], mockCVF(1, 0, 0)]
        (newTimes, newLength) = morph.getTimes(newCvfs, 1, 1)

        (oldTimes, oldLength) = morph.getTimes(self.mockCvfs, 1, 1)

        appendedCvfs = copy.deepcopy(self.mockCvfs)
        appendedCvfs.append(newCvfs[-1])
        (appendedTimes, appendedLength) = morph.getTimes(appendedCvfs, 1, 1)

        self.assertEqual(oldLength + newLength, appendedLength)
        self.assertEqual(appendedTimes[-1] - appendedTimes[-2],
                         newTimes[-1])


class GetTimes_length_test(unittest.TestCase):

    def setUp(self):
        pass

    def test_one_length_cvf_should_have_one_length_times(self):

        mockCvfs = [mockCVF(0, 0, 0)]

        (times, length) = morph.getTimes(mockCvfs, 1, 1)

        self.assertEqual(len(times), 1)
        self.assertEqual(times[0], 0)

    def test_two_length_cvf_should_have_two_length_times(self):
        mockCvfs = [
            mockCVF(0, 0, 0),
            mockCVF(1, 0, 0)
        ]

        (times, length) = morph.getTimes(mockCvfs, 1, 1)
        self.assertEqual(len(times), 2)
        self.assertNotEqual(times[0], times[1])

    def test_last_element_of_times_should_be_fixed_if_fixed_length(self):
        mockCvfs = [
            mockCVF(0, 0, 0),
            mockCVF(1, 0, 0),
            mockCVF(1, 1, 0),
            mockCVF(1, 1, 1)
        ]
        (times, length) = morph.getTimes(mockCvfs, 1, 1, 10)
        self.assertEqual(times[-1], 10)

    def test_fixed_length_times_should_only_differ_in_a_scalar(self):
        mockCvfs = [
            mockCVF(0, 0, 0),
            mockCVF(1, 0, 0),
            mockCVF(1, 1, 0),
            mockCVF(1, 1, 1)
        ]
        (times, length) = morph.getTimes(mockCvfs, 1, 1)
        (fixedTimes, fixedLength) = morph.getTimes(mockCvfs, 1, 1, 10)

        self.assertEqual(length, fixedLength)
        self.assertEqual(len(times), len(fixedTimes))

        scalar = fixedTimes[-1] / times[-1]

        for time, fixedTime in zip(times, fixedTimes):
            if time * fixedTime == 0:
                continue
            self.assertEqual(fixedTime / time, scalar)

    def test_fixed_length_should_also_apply_to_zero_distance_points(self):
        mockCvfs = [
            mockCVF(0, 0, 0),
            mockCVF(0, 0, 0),
            mockCVF(0, 0, 0)
        ]

        (times, length) = morph.getTimes(mockCvfs, 1, 1, 100)
        self.assertEqual(times[0], 0)
        self.assertEqual(times[1], 50)
        self.assertEqual(times[2], 100)


class SunOverrideTest(unittest.TestCase):

    def setUp(self):
        self.scenes = [mockCVF(0,0,0, altitude) for altitude in range(5)]

    def test_increasing_sun_should_stay_the_same(self):
        backup = self.scenes
        morph.overrideSunMovement(self.scenes)
        self.assertListEqual(backup, self.scenes)


class FindFlectionTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_vector_should_return_none(self):
        self.assertIsNone(morph.findInflection([]))

    def test_one_element_vector_should_return_none(self):
        self.assertIsNone(morph.findInflection([5]))

    def test_two_element_vector_should_return_none(self):
        self.assertIsNone(morph.findInflection([4, 3]))

    def test_increasing_vector_should_return_none(self):
        self.assertIsNone(morph.findInflection([1, 2, 3]))

    def test_decreasing_vector_should_return_none(self):
        self.assertIsNone(morph.findInflection([3, 2, 1]))

    def test_downward_inflection_at_second_position_should_return_2(self):
        self.assertEqual(morph.findInflection([1, 2, 1]), 2)

    def test_upwward_inflection_at_second_position_should_return_2(self):
        self.assertEqual(morph.findInflection([1, 0, 1]), 2)

    def test_downward_inflection_at_third_position_should_return_3(self):
        self.assertEqual(morph.findInflection([1, 2, 3, 0]), 3)

    def test_upwward_inflection_at_third_position_should_return_3(self):
        self.assertEqual(morph.findInflection([3, 2, 1, 4]), 3)

class SunOverrideTest(unittest.TestCase):

    def setUp(self):
        self.setSun = mockCVF.setSunAltitude
        self.getSun = mockCVF.getSunAltitude
        mockCVF.setSunAltitude = mock.MagicMock(name='setSunAltitude')
        self.findInflection = morph.findInflection
        morph.findInflection = mock.MagicMock(name='findInflection')

        self.dawn = mockCVF(0, 0, 0, 0)
        self.noon = mockCVF(0, 0, 0, 1.507)
        self.dusk = mockCVF(0, 0, 0, 0)

    def tearDown(self):
        mockCVF.setSunAltitude = self.setSun
        morph.findInflection = self.findInflection

    def test_no_scenes_should_be_overwritten_if_none_are_passed(self):
        self.assertIsNone(morph.overrideSunMovement([]))

    def test_no_scenes_should_be_overwritten_if_one_is_passed(self):
        self.assertIsNone(morph.overrideSunMovement([self.dawn]))
        self.assertFalse(self.dawn.setSunAltitude.called)

    def test_no_scenes_should_be_overwritten_if_two_are_passed(self):
        self.assertIsNone(morph.overrideSunMovement([self.dawn, self.dawn]))
        self.assertFalse(self.dawn.setSunAltitude.called)

    def test_middle_scene_should_be_overwritten_if_decreasing_is_passed(self):
        morph.overrideSunMovement([self.noon, self.dusk, self.dawn])
        mockCVF.setSunAltitude.assert_any_call(1.507/2)

    def test_middle_scene_should_be_overwritten_if_increasing_is_passed(self):
        morph.overrideSunMovement([self.dusk, self.dawn, self.noon])
        mockCVF.setSunAltitude.assert_any_call(1.507/2)

    def test_first_scene_shouldnt_be_overwritten_if_increasing_is_passed(self):
        oldFirst = self.dusk.getSunAltitude()

        morph.overrideSunMovement([self.dusk, self.dusk, self.noon])

        self.assertEqual(self.dusk.getSunAltitude(), oldFirst)

    def test_last_scene_shouldnt_be_overwritten_if_increasing_is_passed(self):
        oldLast = self.noon.getSunAltitude()

        morph.overrideSunMovement([self.dusk, self.dusk, self.noon])

        self.assertEqual(self.noon.getSunAltitude(), oldLast)

    def test_first_scene_shouldnt_be_overwritten_if_decreasing_is_passed(self):
        oldFirst = self.noon.getSunAltitude()

        morph.overrideSunMovement([self.noon, self.dusk, self.dusk])

        self.assertEqual(self.noon.getSunAltitude(), oldFirst)

    def test_last_scene_shouldnt_be_overwritten_if_decreasing_is_passed(self):
        oldLast = self.dusk.getSunAltitude()

        morph.overrideSunMovement([self.noon, self.dusk, self.dusk])

        self.assertEqual(self.dusk.getSunAltitude(), oldLast)

    def test_overrideSunMovement_should_not_call_findInflection_for_short_inputs(self):
        morph.overrideSunMovement([self.noon, self.dusk])
        self.assertFalse(morph.findInflection.called)

    def test_scenes_should_not_be_overwriten_if_4_mountain_is_passed(self):
        first = mockCVF(0, 0, 0, 0)
        second = mockCVF(0, 0, 0, 1)
        third = mockCVF(0, 0, 0, 0.5)
        fourth = mockCVF(0, 0, 0, 0)
        morph.findInflection.return_value = 2
        morph.overrideSunMovement([first, second, third, fourth])

        self.assertEqual(first.getSunAltitude(), 0)
        self.assertEqual(second.getSunAltitude(), 1)
        self.assertEqual(third.getSunAltitude(), 0.5)
        self.assertEqual(fourth.getSunAltitude(), 0)

    def test_scenes_should_not_be_overwriten_if_4_valley_is_passed(self):
        first = mockCVF(0, 0, 0, 1)
        second = mockCVF(0, 0, 0, 0)
        third = mockCVF(0, 0, 0, 0.5)
        fourth = mockCVF(0, 0, 0, 1)
        morph.findInflection.return_value = 2
        morph.overrideSunMovement([first, second, third, fourth])

        self.assertEqual(first.getSunAltitude(), 1)
        self.assertEqual(second.getSunAltitude(), 0)
        self.assertEqual(third.getSunAltitude(), 0.5)
        self.assertEqual(fourth.getSunAltitude(), 1)

    def test_spike_should_create_two_segments(self):
        first = mockCVF(0, 0, 0, 0)
        second = mockCVF(0, 0, 0, 0)
        third = mockCVF(0, 0, 0, 1)
        fourth = mockCVF(0, 0, 0, 0)
        fifth = mockCVF(0, 0, 0, 0)

        mockCVF.setSunAltitude = self.setSun
        morph.findInflection.return_value = 3
        morph.overrideSunMovement([first, second, third, fourth, fifth])

        self.assertEqual(first.getSunAltitude(), 0.0)
        self.assertEqual(second.getSunAltitude(), 0.5)
        self.assertEqual(third.getSunAltitude(), 1.0)
        self.assertEqual(fourth.getSunAltitude(), 0.5)
        self.assertEqual(fifth.getSunAltitude(), 0.0)

    def test_dual_mountain_should_be_handled_right(self):
        first = mockCVF(0, 0, 0, 0)
        second = mockCVF(0, 0, 0, 0)
        third = mockCVF(0, 0, 0, 1)
        fourth = mockCVF(0, 0, 0, 0)
        fifth = mockCVF(0, 0, 0, 0)
        sixth = mockCVF(0, 0, 0, 1)
        seventh = mockCVF(0, 0, 0, 0)

        mockCVF.setSunAltitude = self.setSun
        morph.findInflection = self.findInflection

        morph.overrideSunMovement([first, second, third, fourth, fifth, sixth, seventh])

        self.assertEqual(first.getSunAltitude(), 0)
        self.assertEqual(second.getSunAltitude(), 0.5)
        self.assertEqual(third.getSunAltitude(), 1)
        self.assertEqual(fourth.getSunAltitude(), 0.5)
        self.assertEqual(fifth.getSunAltitude(), 0)
        self.assertEqual(sixth.getSunAltitude(), 1)
        self.assertEqual(seventh.getSunAltitude(), 0)

if __name__ == "__main__":
    unittest.main()
