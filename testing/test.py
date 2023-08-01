# test_my_math.py
import unittest
from my_math import add_numbers

class TestMyMathFunctions(unittest.TestCase):

    def test_add_numbers(self):
        # Test the add_numbers function with different input cases
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)  # Assert that 2 + 3 equals 5

        result = add_numbers(-5, 7)
        self.assertEqual(result, 2)  # Assert that -5 + 7 equals 2

        result = add_numbers(0, 0)
        self.assertEqual(result, 0)  # Assert that 0 + 0 equals 0

if __name__ == '__main__':
    unittest.main()