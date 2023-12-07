import os
import unittest

from day06 import part1, part2


class TestDay06(unittest.TestCase):
    def test_part1(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part1(input_file.readlines()), 288)

    def test_part2(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part2(input_file.readlines()), 71503)


if __name__ == "__main__":
    unittest.main()
