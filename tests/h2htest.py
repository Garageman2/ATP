import unittest
from unittest.mock import patch
from player import Player
import head2head


class MyTestCase(unittest.TestCase):

    def test_inactive(self):
        Roger = Player("Roger Federer")
        self.assertEqual(Roger.career_high, 1)  # add assertion here

    def test_malformed(self):
        with patch('builtins.input',return_value = "Alexander Zverev"):
            Sascha = Player("Sascha Zverev")
            self.assertEqual(Sascha.name,"Alexander Zverev")

    def test_slam_count(self):
        self.assertEqual(Player("Roger Federer").slams, 20)
        self.assertEqual(Player("Gael Monfils").slams, 0)

    def test_fedal(self):
        fedal = head2head.Head2Head(Player("Roger Federer"),Player("Rafael Nadal"))
        fedal.eval()
        self.assertTrue(fedal.score >= 10, "1 Fedal = " + str(fedal.score))

if __name__ == '__main__':
    unittest.main()
