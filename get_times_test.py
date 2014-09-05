import unittest
import morph

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



if __name__ == "__main__":
    unittest.main()
