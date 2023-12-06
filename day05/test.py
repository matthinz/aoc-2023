import os
import unittest

from day05 import part1, part2, Map, MapEntry


class TestDay05(unittest.TestCase):
    def test_mapentry_map_source_to_dest(self):
        # source = 5, 6, 7, 8, 9
        # dest = 25, 26, 27, 28, 29
        e = MapEntry(range(5, 10), 20)

        tests = [
            {
                "input": range(6, 8),
                "expected": (range(0, 0), range(26, 28), range(0, 0)),
            },
            {
                "input": range(0, 8),
                "expected": (range(0, 5), range(25, 28), range(0, 0)),
            },
            {
                "input": range(0, 20),
                "expected": (range(0, 5), range(25, 30), range(10, 20)),
            },
            {
                "input": range(8, 12),
                "expected": (range(0, 0), range(28, 30), range(10, 12)),
            },
            {
                "input": range(44, 48),
                "expected": (range(0, 0), range(0, 0), range(44, 48)),
            },
            {"input": range(0, 4), "expected": (range(0, 4), range(0, 0), range(0, 0))},
        ]

        for t in tests:
            self.assertEqual(t["expected"], e.map_source_to_dest(t["input"]))

    def test_map_trace(self):
        map = Map("soil", "fertilizer")
        map.add(20, 30, 5)  # 20 - 25 --> 30 - 35
        map.add(50, 70, 10)  # 50 - 60 --> 70 - 80

        tests = [
            {
                "input": [range(17, 23), range(50, 65)],
                "expected": [
                    range(17, 20),
                    range(30, 33),
                    range(60, 65),
                    range(70, 80),
                ],
            }
        ]

        for t in tests:
            self.assertEqual(
                t["expected"], sorted(map.trace(t["input"]), key=lambda r: r.start)
            )

    def test_part1(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part1(input_file.readlines()), 35)

    def test_part2(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part2(input_file.readlines()), 46)


if __name__ == "__main__":
    unittest.main()
