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


def parse_input(lines: list[str]) -> (int, int, list[list[str]]):
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    grid = [list(line) for line in lines]
    grid_width = len(grid[0])
    grid_height = len(grid)

    for row in grid:
        assert len(row) == grid_width

    return (grid_width, grid_height, grid)


def count_energized_tiles(
    grid: list[list[str]], initial_pos: Point, initial_vector: Point
) -> int:
    grid_height = len(grid)
    grid_width = len(grid[0])

    positions: list[Point] = [initial_pos]
    vectors: list[Point] = [initial_vector]
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


def part1(lines: list[str]) -> Optional[int]:
    _, _, grid = parse_input(lines)
    return count_energized_tiles(grid, (0, 0), RIGHT)


def part2(lines: list[str]) -> Optional[int]:
    grid_width, grid_height, grid = parse_input(lines)

    best_score: Optional[int] = None

    candidates = [
        *(((x, 0), DOWN) for x in range(grid_width)),
        *(((0, y), RIGHT) for y in range(grid_height)),
        *(((x, grid_height - 1), UP) for x in range(grid_width)),
        *(((grid_width - 1, y), LEFT) for y in range(grid_height)),
    ]

    for initial_pos, initial_vector in candidates:
        score = count_energized_tiles(grid, initial_pos, initial_vector)
        if best_score is None or score > best_score:
            best_score = score

    return best_score


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
