import os
import unittest

from day10 import part1, part2

TEST_INPUT = """
    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
"""


class TestDay10(unittest.TestCase):
    def test_part1(self):
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 8)

    def test_part2(self):
        lines = [line.strip() for line in TEST_INPUT.split("\n")]

        self.assertEqual(part2(lines), None)


if __name__ == "__main__":
    unittest.main()
