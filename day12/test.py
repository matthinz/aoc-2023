import unittest

from day12 import part1, part2, parse_input, count_solutions, find_possible_variants, is_valid


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

    def test_find_possible_variants(self):
        tests = [
            {
                "input": "##?#?#",
                "expected": [
                    "##.#.#",
                    "####.#",
                    "##.###",
                    "######",
                ],
            },
            {"input": "#####", "expected": ["#####"]},
            {"input": "?", "expected": ["#", "."]},
        ]

        for i, test in enumerate(tests):
            actual = list(sorted(find_possible_variants(test["input"])))
            expected = list(sorted(test["expected"]))
            self.assertEqual(expected, actual, f"Test {i+1} (\"{test["input"]}\")")

    def test_is_valid(self):
        tests = [
            ("###", [3], True),
            ("###", [2], False),
            ("###", [4], False),
            ("##.#.#", [2,1,1], True),
            ("##.#.#", [3,1,1], False),
            ("##.#.#", [2,2,1], False),
            ("##.#.#", [2,1,2], False),
        ]

        for conditions, sizes, expected in tests:
            actual = is_valid(conditions, sizes)
            self.assertEqual(expected, actual)


    def test_count_solutions(self):
        tests = [
            {"input": "?###?#????.?.#????# 10,1,1,1,1", "expected": 2},
            {"input": "?.?????#??#?#???? 1,1,1,1,4", "expected": 13},
            {"input": ".?.#??.??.? 2,1", "expected": 3},
        ]

        for test in tests:
            solutions = []

            for conditions, sizes in parse_input([test["input"]]):
                solutions.append(count_solutions(conditions, sizes))

            actual = sum(solutions)

            self.assertEqual(actual, test["expected"])

    def test_part2(self):
        TEST_INPUT = """
        """

        lines = [line.strip() for line in TEST_INPUT.split("\n")]
        self.assertEqual(part2(lines), None)


if __name__ == "__main__":
    unittest.main()
