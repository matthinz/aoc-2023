import unittest

from day15 import (
    part1,
    part2,
)


class TestDay15(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = """
            rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 1320)

    def test_part2(self):
        TEST_INPUT = """
            rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), 145)


if __name__ == "__main__":
    unittest.main()
