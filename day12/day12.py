from math import ceil
import sys
from itertools import combinations
from typing import Iterator, Optional


def parse_input(
    lines: list[str], unfolding_factor: int = 1
) -> Iterator[tuple[str, list[int]]]:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")

    for line in lines:
        conditions, sizes = line.split(" ")

        conditions = "?".join([conditions] * unfolding_factor)

        sizes = [int(value) for value in sizes.split(",")]
        sizes *= unfolding_factor

        yield (conditions, sizes)


def optimize_unknown_indices(conditions: str, sizes: list[int]) -> tuple[str, set[int]]:
    unknown_indices = [i for i, _ in enumerate(conditions) if conditions[i] == "?"]

    def set_index(conditions: str, i: int, value: str) -> str:
        result = list(conditions)
        result[i] = value
        return "".join(result)

    def break_into_runs(conditions: str) -> list[str]:
        return [r for r in conditions.split(".") if r != ""]

    def is_possible(index: int, state: str) -> bool:
        working_conditions = set_index(conditions, index, state)
        runs = break_into_runs(working_conditions)

        # The cases here:
        # 1. runs[0] is all unknown (e.g. '???')
        # 2. runs[0] is all damaged (e.g. '###')
        # 3. runs[0] is a mix (e.g. '?#?#')
        #
        any_unknown = "?" in runs[0]
        any_damaged = "#" in runs[0]
        all_damaged = not any_unknown
        if all_damaged:
            # We know that the corresponding size must match this run's
            # length exactly
            if sizes[0] != len(runs[0]):
                return False
        elif any_unknown and any_damaged:
            # This is a mix of damaged and unknown.
            # This run is possible only if the size required <= the length
            # of the run
            if sizes[0] > len(runs[0]):
                return False

        return True

    i = 0
    while i < len(unknown_indices):
        unknown_index = unknown_indices[0]
        damaged_is_possible = is_possible(unknown_index, "#")
        undamaged_is_possible = is_possible(unknown_index, ".")

        if damaged_is_possible and not undamaged_is_possible:
            # This index must be damaged
            conditions = set_index(conditions, unknown_index, "#")
            unknown_indices[0:1] = []
            continue
        elif undamaged_is_possible and not damaged_is_possible:
            conditions = set_index(conditions, unknown_index, ".")
            unknown_indices[0:1] = []
            continue

        i += 1

    return (conditions, set(unknown_indices))


def find_possible_variants(conditions: str, sizes: list[int]) -> Iterator[str]:
    """
    Given a conditions string, returns an Iterator that runs through the
    different ways "?" could be filled in
    """

    conditions, unknown_indices = optimize_unknown_indices(conditions, sizes)

    if len(unknown_indices) == 0:
        yield conditions
        return

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
    for conditions in find_possible_variants(input_conditions, sizes):
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
