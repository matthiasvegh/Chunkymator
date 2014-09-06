import unittest
import morph
import copy

class mockCVF:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z

class GetTimes_consistency_test(unittest.TestCase):

    def setUp(self):
        tuples = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        self.mockCvfs = [mockCVF(*t) for t in tuples]

    def test_doubling_of_frame_rate_should_double_times(self):

        rate1 = 1
        rate2 = 2*rate1

        (times1, length1) = morph.getTimes(self.mockCvfs, rate1, 1)
        (times2, length2) = morph.getTimes(self.mockCvfs, rate2, 1)

        for t1, t2 in zip(times1, times2):
            self.assertEqual(t1*2, t2)

    def test_doubling_of_frame_rate_should_not_influence_total_length(self):

        rate1 = 1
        rate2 = 2*rate1

        (times1, length1) = morph.getTimes(self.mockCvfs, rate1, 1)
        (times2, length2) = morph.getTimes(self.mockCvfs, rate2, 1)

        self.assertEqual(length1, length2)

    def test_doubling_speed_should_halve_times(self):

        speed1 = 1
        speed2 = 2*speed1

        (times1, length1) = morph.getTimes(self.mockCvfs, 1, speed1)
        (times2, length2) = morph.getTimes(self.mockCvfs, 1, speed2)

        for t1, t2 in zip(times1, times2):
            self.assertEqual(t1, t2*2)

    def test_appending_to_input_should_append_to_time(self):

        newCvfs = copy.deepcopy(self.mockCvfs)
        newCvfs.append(mockCVF(4, 0, 0))

        (oldTimes, oldLength) = morph.getTimes(self.mockCvfs, 1, 1)
        (newTimes, newLength) = morph.getTimes(newCvfs, 1, 1)

        for (old, new) in zip(oldTimes, newTimes):
            self.assertEqual(old, new)

        self.assertGreater(newTimes[-1], oldTimes[-1])
        self.assertEqual(len(oldTimes) +1, len(newTimes))


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

if __name__ == "__main__":
    unittest.main()
