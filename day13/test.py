import unittest

from day13 import (
    part1,
    part2,
)


class TestDay13(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = """
            #.##..##.
            ..#.##.#.
            ##......#
            ##......#
            ..#.##.#.
            ..##..##.
            #.#.##.#.

            #...##..#
            #....#..#
            ..##..###
            #####.##.
            #####.##.
            ..##..###
            #....#..#
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 405)

    def test_part2(self):
        TEST_INPUT = """
        """

        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), None)


if __name__ == "__main__":
    unittest.main()
