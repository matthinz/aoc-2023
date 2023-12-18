from math import ceil
import sys
from itertools import combinations
from typing import Iterator, Optional


def parse_input(lines: list[str]) -> Iterator[list[str]]:
    lines = (line.strip() for line in lines)

    current: list[str] = []

    for line in lines:
        if line == "":
            if len(current) > 0:
                yield current
                current = []
        else:
            current.append(line)

    if len(current) > 0:
        yield current


def rows(grid: list[str]) -> Iterator[str]:
    for row in grid:
        yield row


def cols(grid: list[str]) -> Iterator[str]:
    i = 0
    while True:
        col: list[str] = []
        for row in grid:
            if i >= len(row):
                return
            col.append(row[i])
        yield col
        i += 1


def find_reflections(line: list[str]) -> Iterator[int]:
    """
    Finds points on <line> where a symmetry exists on the left and right sides.
    """
    for i in range(1, len(line)):
        symmetrical = True
        for j in range(0, i):
            left = i - j - 1
            right = i + j
            if left < 0 or right >= len(line):
                break

            if line[left] != line[right]:
                symmetrical = False
                break

        if symmetrical:
            yield i


def find_line_of_reflection(lines: Iterator[str]) -> Optional[int]:
    indices: Optional[set[int]] = None

    for line in lines:
        if indices is None:
            indices = set(i for i in range(0, len(line)))

        indices = indices & set(find_reflections(line))

        if len(indices) == 0:
            break

    if len(indices) == 1:
        return indices.pop()


def part1(lines: list[str]) -> Optional[int]:
    result = 0

    for pattern in parse_input(lines):
        vertical_line = find_line_of_reflection(rows(pattern))

        if vertical_line is not None:
            result += vertical_line
            continue

        horizontal_line = find_line_of_reflection(cols(pattern))
        if horizontal_line is not None:
            result += 100 * horizontal_line
            continue

        print("\n".join(pattern))
        assert False, "No line present in pattern"

    return result


def part2(lines: list[str]) -> Optional[int]:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
