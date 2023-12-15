from math import ceil
import sys
from itertools import combinations
from typing import Iterator, Optional


def parse_input(lines: list[str]) -> Iterator[tuple[str, list[int]]]:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    for line in lines:
        conditions, sizes = line.split(" ")
        yield (conditions, [int(value) for value in sizes.split(",")])


@staticmethod
def find_possible_variants(conditions: str) -> Iterator[str]:
    """
    Given a conditions string, returns an Iterator that runs through the
    different ways "?" could be filled in
    """
    unknown_indices = set(i for i, _ in enumerate(conditions) if conditions[i] == "?")

    for damaged_count in range(0, len(unknown_indices) + 1):
        for damaged_indices in combinations(unknown_indices, damaged_count):
            damaged_indices = set(damaged_indices)
            new_conditions = list(conditions)
            for i in unknown_indices:
                new_conditions[i] = "#" if i in damaged_indices else "."
            yield "".join(new_conditions)


def is_valid(conditions: str, sizes: list[int]) -> int:
    runs = [r for r in conditions.split(".") if r != ""]

    if len(runs) != len(sizes):
        return False

    for run, size in zip(runs, sizes):
        if len(run) != size:
            return False

    return True


def count_solutions(input_conditions: str, sizes: list[int]) -> int:
    result = 0
    for conditions in find_possible_variants(input_conditions):
        if is_valid(conditions, sizes):
            result += 1
    return result


def part1(lines: list[str]) -> Optional[int]:
    result = 0

    for conditions, sizes in parse_input(lines):
        result += count_solutions(conditions, sizes)

    return result


def part2(lines: list[str]) -> Optional[int]:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
