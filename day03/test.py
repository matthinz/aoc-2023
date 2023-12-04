import os
import unittest

from day03 import part1, part2


class TestDay03(unittest.TestCase):
    def test_part1(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part1(input_file.readlines()), 4361)

    def test_part1_with_negatives(self):
        input = """
        434..-49.
        ....$90..
        """
        lines = [line.strip() for line in input.strip().split("\n")]
        self.assertEqual(part1(lines), 139)

    def test_parse_example_from_reddit(self):
        input = """
            12.......*..
            +.........34
            .......-12..
            ..78........
            ..*....60...
            78.........9
            .5.....23..$
            8...90*12...
            ............
            2.2......12.
            .*.........*
            1.1..503+.56
        """
        lines = [line.strip() for line in input.strip().split("\n")]
        self.assertEqual(part1(lines), 925)

    def test_part2(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part2(input_file.readlines()), 467835)


if __name__ == "__main__":
    unittest.main()
