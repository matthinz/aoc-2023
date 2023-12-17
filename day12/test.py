import unittest

from day12 import (
    part1,
    part2,
    parse_input,
    count_solutions
)


class TestDay12(unittest.TestCase):
    def test_part1(self):
        TEST_INPUT = """
            ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1
        """
        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part1(lines), 21)


    def test_count_solutions(self):

        tests = [
            # {"input": "?###?#????.?.#????# 10,1,1,1,1", "expected": 2},
            {"input": "?.????? 1,1", "expected": 11},
            {"input": "?.?????#??#?#???? 1,1,1,1,4", "expected": 13},
            {"input": ".?.#??.??.? 2,1", "expected": 3},
            {"input": "???.????.?..????? 3,1,1,3", "expected": 28},
        ]

        for test in tests:
            solutions = []

            for conditions, sizes in parse_input([test["input"]]):
                solutions.append(count_solutions(conditions, sizes))

            actual = sum(solutions)

            self.assertEqual(actual, test["expected"], f"{test["input"]} should have {test["expected"]} solutions")

    def test_part2(self):
        TEST_INPUT = """
        """

        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), None)


if __name__ == "__main__":
    unittest.main()
