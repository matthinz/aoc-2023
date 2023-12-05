import os
import unittest

from day05 import part1, part2


class TestDay05(unittest.TestCase):
    def test_part1(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part1(input_file.readlines()), 35)

    def test_part2(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part2(input_file.readlines()), None)


if __name__ == "__main__":
    unittest.main()
