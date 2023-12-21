import sys
from enum import Enum
from typing import Iterator, Optional


class Rock(Enum):
    ROUND = 1
    CUBE = 2


type GridRow = list[Optional[Rock]]
type Grid = list[GridRow]


def parse_input(lines: Iterator[str]) -> Grid:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    grid: Grid = []
    for line in lines:
        if line == "":
            continue

        row: GridRow = []
        for c in line:
            match c:
                case ".":
                    row.append(None)
                case "#":
                    row.append(Rock.CUBE)
                case "O":
                    row.append(Rock.ROUND)
                case _:
                    assert False

        grid.append(row)

    return grid


def part1(lines: list[str]) -> Optional[int]:
    grid = parse_input(lines)
    height = len(grid)
    load = 0

    for y, row in enumerate(grid):
        for x, r in enumerate(row):
            if r != Rock.ROUND:
                continue

            # This rock's ultimate position will be at the nearest #
            # at this same x or 0
            nearest_cube_shaped_rock = None
            nearest_rounded_rock = None
            probe_y = y - 1
            while probe_y >= 0:
                probe = grid[probe_y][x]
                if probe == Rock.CUBE:
                    nearest_cube_shaped_rock = probe_y
                    break
                elif probe == Rock.ROUND:
                    nearest_rounded_rock = probe_y
                    break
                probe_y -= 1

            if nearest_cube_shaped_rock is not None:
                grid[y][x] = "."
                grid[nearest_cube_shaped_rock + 1][x] = Rock.ROUND

                load += height - (nearest_cube_shaped_rock + 1)
            elif nearest_rounded_rock is not None:
                grid[y][x] = "."
                grid[nearest_rounded_rock + 1][x] = Rock.ROUND

                load += height - (nearest_rounded_rock + 1)
            else:
                grid[y][x] = None
                grid[0][x] = Rock.ROUND
                load += height

    return load


def part2(lines: list[str]) -> Optional[int]:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
