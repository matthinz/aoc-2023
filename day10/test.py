import os
import unittest

from day10 import part1, part2


class TestDay10(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = """
            ..F7.
            .FJ|.
            SJ.L7
            |F--J
            LJ...
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 8)

    def test_part2_squeaking(self):
        TEST_INPUT = """
            ..........
            .S------7.
            .|F----7|.
            .||....||.
            .||....||.
            .|L-7F-J|.
            .|..||..|.
            .L--JL--J.
            ..........
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), 4)

    def test_part2(self):
        TEST_INPUT = """
            FF7FSF7F7F7F7F7F---7
            L|LJ||||||||||||F--J
            FL-7LJLJ||||||LJL-77
            F--JF--7||LJLJ7F7FJ-
            L---JF-JLJ.||-FJLJJ7
            |F|F-JF---7F7-L7L|7|
            |FFJF7L7F-JF7|JL---7
            7-L-JL7||F7|L7F-7F7|
            L.L7LFJ|||||FJL7||LJ
            L7JLJL-JLJLJL--JLJ.L
        """

        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), 10)


if __name__ == "__main__":
    unittest.main()
