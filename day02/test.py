import os
import unittest

from day02 import (
    game_is_possible,
    min_cubes_required,
    parse_game,
    parse_round,
    part2,
    part1,
    round_is_possible,
)


class TestDay02(unittest.TestCase):
    def test_parse_round(self):
        input = "2 blue, 4 red, 110 yellow"
        expected = {"blue": 2, "red": 4, "yellow": 110}
        self.assertEqual(parse_round(input), expected)

    def test_parse_game(self):
        input = (
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
        )
        expected = {
            "id": 3,
            "rounds": [
                {"green": 8, "blue": 6, "red": 20},
                {"blue": 5, "red": 4, "green": 13},
                {"green": 5, "red": 1},
            ],
        }
        self.assertEqual(parse_game(input), expected)

    def test_part1_game_is_possible(self):
        maxes = {"red": 12, "green": 13, "blue": 14}
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            games = [parse_game(line) for line in input_file.readlines()]
            possibles = [game["id"] for game in games if game_is_possible(game, maxes)]
            self.assertEqual(possibles, [1, 2, 5])

    def test_round_is_possible(self):
        maxes = {"red": 12, "green": 13, "blue": 14}
        game = parse_game(
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
        )
        self.assertFalse(round_is_possible(game["rounds"][0], maxes))
        self.assertTrue(round_is_possible(game["rounds"][1], maxes))

    def test_round_is_possible_boundary(self):
        maxes = {"red": 12, "green": 13, "blue": 14}
        game = parse_game("Game 3: 13 green, 14 blue, 12 red")
        self.assertTrue(round_is_possible(game["rounds"][0], maxes))

    def test_part1(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part1(input_file.readlines()), 8)

    def test_min_cubes_required(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            games = [parse_game(line) for line in input_file.readlines()]
            actual = [min_cubes_required(game) for game in games]
            expected = [
                {"red": 4, "green": 2, "blue": 6},
                {"red": 1, "green": 3, "blue": 4},
                {"red": 20, "green": 13, "blue": 6},
                {"red": 14, "green": 3, "blue": 15},
                {"red": 6, "green": 3, "blue": 2},
            ]
            self.assertEqual(expected, actual)

    def test_part2(self):
        input_filename = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(input_filename, "r") as input_file:
            self.assertEqual(part2(input_file.readlines()), 2286)


if __name__ == "__main__":
    unittest.main()
