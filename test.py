import unittest
import morph

class TestNormalizeFunction(unittest.TestCase):

    def setUp(self):
        self.list = [0, 90, 290, 350, 45, 0]
        self.ammount = 180

    def test_normalize(self):
        morph.normalize(self.list, self.ammount)

        self.assertSequenceEqual(self.list, [0, 90, -70, -10, 45, 0])

class MockSpline:
	def __init__(self, *params):
		self.list = []
		for p in params:
			self.list.append(p)

	def __call__(self, index):
		return self.list[index]

class CameraAnglesTest(unittest.TestCase):

	def setUp(self):
		pass

	def test_camera_angles_on_a_straight_line_should_look_forward(self):
		xSpline = MockSpline(1, 2, 3, 4)
		ySpline = MockSpline(0, 0, 0, 0)
		zSpline = MockSpline(0, 0, 0, 0)

		result = morph.getCameraAngles(xSpline, ySpline, zSpline, [0, 1, 2, 3])

		(yaws, pitches) = result

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 180)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 270)

if __name__ == "__main__":
    unittest.main()
