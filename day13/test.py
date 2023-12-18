import unittest

from day13 import (
    part1,
    part2,
    find_variant_patterns,
    parse_input,
    Direction,
    find_lines_of_reflection_in_pattern,
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
        self.assertEqual(part2(lines), 400)

    def test_find_variant(self):
        TEST_INPUT = """
            .##......
            ###.####.
            ##.##...#
            ..###..##
            ...##..##
            #..#.##.#
            ..#......
            .##..##..
            .##..##..
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]

        for pattern in parse_input(lines):
            variants = list(find_variant_patterns(pattern))
            self.assertEqual(81, len(variants))
            for variant, _, _ in variants:
                self.assertNotEqual("\n".join(variant), "\n".join(pattern))

    def test_part2_variant_that_didnt_work_for_some_reason(self):
        TEST_INPUT = """
            .......####..##..
            .####.##.#.#....#
            .####...#.#.####.
            ######.##.#######
            ........#..#....#
            .####....########
            ......###.###..##
            #....##.###......
            .####...#.###..##
            #....####.##....#
            ........##.######
            ##..##.####.####.
            ######..#....##..
            #....#..####....#
            .####.##.#.######
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]

        patterns = list(parse_input(lines))
        self.assertEqual(1, len(patterns))

        lines = list(find_lines_of_reflection_in_pattern(patterns[0]))

        self.assertEqual([(3, Direction.VERTICAL), (14, Direction.VERTICAL)], lines)

    def test_part2_examples_from_reddit(self):
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

            .#.##.#.#
            .##..##..
            .#.##.#..
            #......##
            #......##
            .#.##.#..
            .##..##.#

            #..#....#
            ###..##..
            .##.#####
            .##.#####
            ###..##..
            #..#....#
            #..##...#
        """

        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), 1400)


if __name__ == "__main__":
    unittest.main()
