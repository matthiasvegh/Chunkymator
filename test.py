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

class StraightLineCameraAnglesTest(unittest.TestCase):

	def setUp(self):
		self.increasingSpline = MockSpline(1, 2, 3, 4)
		self.sameSpline = MockSpline(0, 0, 0, 0)
		self.times = [0, 1, 2, 3]

	def test_camera_angles_on_increasing_x_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.increasingSpline,
				self.sameSpline,
				self.sameSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 180)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 270)

	def test_camera_angles_on_increasing_y_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.sameSpline,
				self.increasingSpline,
				self.sameSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 90)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 180)


if __name__ == "__main__":
    unittest.main()
