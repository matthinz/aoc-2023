import unittest

from day14 import (
    part1,
    part2,
)


class TestDay14(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = """
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 136)

    def test_part2(self):
        TEST_INPUT = """
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), 64)


if __name__ == "__main__":
    unittest.main()
