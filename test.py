import unittest
import morph

class TestNormalizeFunction(unittest.TestCase):

    def setUp(self):
        self.list = [0, 90, 290, 350, 45, 0]
        self.ammount = 180

    def test_normalize(self):
        morph.normalize(self.list, self.ammount)

        self.assertSequenceEqual(self.list, [0, 90, -70, -10, 45, 0])

if __name__ == "__main__":
    unittest.main()
