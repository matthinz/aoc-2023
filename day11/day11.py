from math import floor, sqrt
import sys
from functools import cmp_to_key
from itertools import combinations
from typing import Iterator, Optional

INFINITY = float("inf")


class Point:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def north(self) -> "Point":
        return Point(self.x, self.y - 1)

    @property
    def south(self) -> "Point":
        return Point(self.x, self.y + 1)

    @property
    def east(self) -> "Point":
        return Point(self.x + 1, self.y)

    @property
    def west(self) -> "Point":
        return Point(self.x - 1, self.y)

    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Galaxy:
    def __init__(self, number: int, position: Point) -> None:
        self.number = number
        self.position = position


def parse_input(lines: list[str], expansion_factor: int) -> dict[int, Point]:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    galaxies_by_row: dict[int, int] = {}
    galaxies_by_col: dict[int, int] = {}
    galaxy_positions: dict[int, Point] = {}

    last_galaxy_index = 0

    for y, line in enumerate(lines):
        galaxies_by_row[y] = 0
        for x, c in enumerate(line):
            if y == 0:
                galaxies_by_col[x] = 0

            if c == "#":
                last_galaxy_index += 1
                galaxy_positions[last_galaxy_index] = Point(x, y)
                galaxies_by_row[y] += 1
                galaxies_by_col[x] += 1

    empty_rows = sorted([y for y in galaxies_by_row if galaxies_by_row[y] == 0])
    empty_cols = sorted([x for x in galaxies_by_col if galaxies_by_col[x] == 0])

    for galaxy, position in galaxy_positions.items():
        # For each empty column before this galaxy's x position,
        # add <expansion_factor> to its x
        new_position = position

        for empty_col in empty_cols:
            if empty_col < position.x:
                new_position = Point(
                    new_position.x + expansion_factor - 1, new_position.y
                )

        for empty_row in empty_rows:
            if empty_row < position.y:
                new_position = Point(
                    new_position.x, new_position.y + expansion_factor - 1
                )

        galaxy_positions[galaxy] = new_position

    return galaxy_positions


def steps_between(a: Point, b: Point) -> int:
    return abs(b.y - a.y) + abs(b.x - a.x)


def part1(lines: list[str]) -> int:
    galaxy_positions = parse_input(lines, expansion_factor=2)

    combos = list(combinations(galaxy_positions.keys(), 2))

    distances = (
        steps_between(galaxy_positions[a], galaxy_positions[b]) for a, b in combos
    )

    return sum(distances)


def part2(lines: list[str], expansion_factor: int = 1_000_000) -> int:
    galaxy_positions = parse_input(lines, expansion_factor=expansion_factor)

    combos = list(combinations(galaxy_positions.keys(), 2))

    distances = (
        steps_between(galaxy_positions[a], galaxy_positions[b]) for a, b in combos
    )

    return sum(distances)


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
