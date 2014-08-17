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
		self.decreasingSpline = MockSpline(4, 3, 2, 1)
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


	def test_camera_angles_on_increasing_z_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.sameSpline,
				self.sameSpline,
				self.increasingSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 90)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 270)


	def test_camera_angles_on_decreasing_x_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.decreasingSpline,
				self.sameSpline,
				self.sameSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 0)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 270)

	def test_camera_angles_on_decreasing_y_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.sameSpline,
				self.decreasingSpline,
				self.sameSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 90)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 0)


	def test_camera_angles_on_decreasing_z_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.sameSpline,
				self.sameSpline,
				self.decreasingSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 270)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 270)

	def test_camera_angles_on_increasing_x_and_y_should_look_forward(self):
		(yaws, pitches) = morph.getCameraAngles(
				self.increasingSpline,
				self.increasingSpline,
				self.sameSpline,
				self.times)

		self.assertEqual(len(yaws), 4)
		self.assertEqual(len(pitches), 4)

		for yaw in yaws:
			self.assertAlmostEqual(yaw, 180)

		for pitch in pitches:
			self.assertAlmostEqual(pitch, 225)


class RegularSplineTest(unittest.TestCase):

    def setUp(self):
        self.times = [0, 1, 3, 5]
        self.sameVals = [0, 0, 0, 0]
        self.increasing = [0, 1, 3, 5]
        self.result = morph.createRegularSpline(self.times, self.increasing)

    def test_control_points_on_spline_are_same_as_input(self):

        for i in range(len(self.times)):
            time = self.times[i]
            expectedValue = self.increasing[i]
            self.assertAlmostEqual(self.result(time), expectedValue)

    def test_points_on_spline_should_be_between_control_points(self):

        for i in range(len(self.times) -1):
            previousTime = self.times[i]
            nextTime = self.times[i+1]
            currentTime = float(nextTime + previousTime)/2

            previousValue = self.result(previousTime)
            nextValue = self.result(nextTime)
            currentValue = self.result(currentTime)

            self.assertTrue(previousValue < currentValue and currentValue < nextValue)


if __name__ == "__main__":
    unittest.main()
