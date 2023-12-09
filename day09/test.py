import os
import unittest

from day09 import part1, part2

TEST_INPUT = """
    0   3   6   9  12  15
    1   3   6  10  15  21
    10  13  16  21  30  45
"""


class TestDay09(unittest.TestCase):
    def test_part1(self):
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 114)

    def test_part2(self):
        lines = [line.strip() for line in TEST_INPUT.split("\n")]

        self.assertEqual(part2(lines), 2)


if __name__ == "__main__":
    unittest.main()
