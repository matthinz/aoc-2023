from functools import reduce
import sys
from enum import Enum
from typing import Callable, Iterator, Literal, Optional

type Point = tuple[int, int]
X = 0
Y = 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

REFLECTIONS: dict[Literal["/"] | Literal["\\"], dict[Point, Point]] = {
    "/": {UP: RIGHT, DOWN: LEFT, LEFT: DOWN, RIGHT: UP},
    "\\": {UP: LEFT, DOWN: RIGHT, LEFT: UP, RIGHT: DOWN},
}


def part1(lines: list[str]) -> Optional[int]:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    grid = [list(line) for line in lines]

    grid_height = len(grid)
    grid_width = len(grid[0])

    for row in grid:
        assert len(row) == grid_width

    positions: list[Point] = [(0, 0)]
    vectors: list[Point] = [(1, 0)]
    energized: set[Point] = set(positions)
    visited: set[tuple[Point, Point]] = set()

    while len(positions) > 0:
        p = positions[0]
        v = vectors[0]

        p = (p[X] + v[X], p[Y] + v[Y])

        outside_grid = p[X] < 0 or p[Y] < 0 or p[X] >= grid_width or p[Y] >= grid_height
        if outside_grid:
            del positions[0]
            del vectors[0]
            continue

        p_v = (p, v)
        if p_v in visited:
            # We are in a loop
            del positions[0]
            del vectors[0]
            continue

        visited.add(p_v)
        energized.add(p)

        positions[0] = p

        tile = grid[p[Y]][p[X]]

        match tile:
            case ".":
                pass

            case "/" | "\\":
                v = REFLECTIONS[tile][v]

            case "-":
                if v == UP or v == DOWN:
                    # This one moves left, add another moving right
                    v = LEFT
                    positions.append(p)
                    vectors.append(RIGHT)

            case "|":
                if v == LEFT or v == RIGHT:
                    # This one moves up, add another moving down
                    v = UP
                    positions.append(p)
                    vectors.append(DOWN)

            case _:
                assert False

        vectors[0] = v

    return len(energized)


def part2(lines: list[str]) -> Optional[int]:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
