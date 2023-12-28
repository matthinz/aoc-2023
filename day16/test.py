import unittest

from day16 import (
    part1,
    part2,
)


class TestDay16(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = r"""
            .|...\....
            |.-.\.....
            .....|-...
            ........|.
            ..........
            .........\
            ..../.\\..
            .-.-/..|..
            .|....-|.\
            ..//.|....
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 46)

    def test_part2(self):
        TEST_INPUT = """
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), None)


if __name__ == "__main__":
    unittest.main()
