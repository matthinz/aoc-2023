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


def parse_input(lines: list[str]) -> set[Galaxy]:
    grid: list[list[Optional[int]]] = []
    last_galaxy_index = 0
    galaxies: set[Galaxy] = set()

    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    for y, line in enumerate(lines):
        row: list[Optional[Galaxy]] = []
        grid.append(row)
        any_galaxies_in_row = False

        for x, c in enumerate(line):
            if c == "#":
                last_galaxy_index += 1
                galaxy = Galaxy(last_galaxy_index, Point(x, y))
                galaxies.add(galaxy)
                row.append(galaxy)
                any_galaxies_in_row = True
            else:
                row.append(None)

        if not any_galaxies_in_row:
            grid.append([*row])

    assert len(grid) > 0
    assert len(grid[0]) > 0

    x = 0
    while x < len(grid[0]):
        any_galaxies_in_col = False
        for row in grid:
            if row[x]:
                any_galaxies_in_col = True
                break

        if any_galaxies_in_col:
            x += 1
            continue

        for row in grid:
            row.insert(x, None)
        x += 2

    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if isinstance(v, Galaxy):
                v.position = Point(x, y)

    return galaxies


def format_grid(
    grid: list[list[Optional[Galaxy]]], path: Optional[list[Point]] = None
) -> str:
    result = []
    for y, row in enumerate(grid):
        line = []
        for x, v in enumerate(row):
            if path and (x, y) in path:
                line.append("*")
            elif v:
                line.append(str(v.number))
            else:
                line.append(".")
        result.append("".join(line))
    return "\n".join(result)


def print_grid(grid: list[list[Optional[Galaxy]]], path: Optional[list[Point]] = None):
    print(f"\n{format_grid(grid, path)}\n")


def steps_between(a: Point, b: Point) -> int:
    return abs(b.y - a.y) + abs(b.x - a.x)


def part1(lines: list[str]) -> int:
    galaxies = parse_input(lines)

    combos = list(combinations(galaxies, 2))

    distances = (
        steps_between(galaxy_a.position, galaxy_b.position)
        for galaxy_a, galaxy_b in combos
    )

    return sum(distances)


def part2(lines) -> int:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
