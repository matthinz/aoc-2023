import os
import unittest

from day08 import part1, part2


class TestDay08(unittest.TestCase):
    def test_part1(self):
        test_input = """
            LLR

            AAA = (BBB, BBB)
            BBB = (AAA, ZZZ)
            ZZZ = (ZZZ, ZZZ)
        """

        lines = [line.strip() for line in test_input.split("\n")]

        self.assertEqual(part1(lines), 6)

    def test_part2(self):
        test_input = """
            LR

            11A = (11B, XXX)
            11B = (XXX, 11Z)
            11Z = (11B, XXX)
            22A = (22B, XXX)
            22B = (22C, 22C)
            22C = (22Z, 22Z)
            22Z = (22B, 22B)
            XXX = (XXX, XXX)
        """

        lines = [line.strip() for line in test_input.split("\n")]

        self.assertEqual(part2(lines), 6)


if __name__ == "__main__":
    unittest.main()
