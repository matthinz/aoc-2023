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


def count_solutions_in_branch(
    conditions: str, sizes: list[int], cache: dict[str, int]
) -> int:
    conditions = conditions.strip(".")
    i = conditions.find(".")
    first_run = conditions[0:i] if i >= 0 else conditions

    if len(sizes) == 0:
        return 0

    if len(conditions) == 0:
        return 0

    expected_size = sizes[0]

    any_unknown = "?" in first_run
    all_damaged = not any_unknown

    # If the first run is all damaged, but does not match the expected size,
    # then there are no solutions down this branch.
    if all_damaged:
        if len(first_run) == expected_size:
            # This solution fits (so far), so we can continue down this branch,
            # skipping the first run to limit the search space.
            next_conditions = conditions[len(first_run) :].strip(".")
            next_sizes = sizes[1:]

            return count_solutions(next_conditions, next_sizes, cache)
        else:
            # There are no solutions down this branch

            return 0
    else:
        return count_solutions(conditions, sizes, cache)


def count_solutions(
    conditions: str, sizes: list[int], cache: dict[str, int] = {}
) -> int:
    unknown_indices = [i for i, _ in enumerate(conditions) if conditions[i] == "?"]

    if len(unknown_indices) == 0:
        # Check if this is an actual solution
        runs = [r for r in conditions.split(".") if r != ""]
        if len(runs) != len(sizes):
            return 0

        for run, expected_size in zip(runs, sizes):
            if len(run) != expected_size:
                return 0

        return 1

    match len(sizes):
        case 0:
            any_damaged = "#" in conditions

            if any_damaged:
                return 0

            return 1

        case 1:
            max_damaged = sizes[0]
            actual_damaged = len([c for c in conditions if c == "#"])

            if actual_damaged > max_damaged:
                return 0

    for size in sizes:
        if size > len(conditions):
            return 0

    leading_damaged = 0
    for c in conditions:
        if c == "#":
            leading_damaged += 1
        else:
            break

    if leading_damaged > sizes[0]:
        return 0

    damaged_or_unknown = conditions.replace(".", "")

    # For a set of sizes of length n, the minimum length of the
    # conditions string is n + n-1
    if len(conditions) < (len(sizes) * 2) - 1:
        return 0

    if len(damaged_or_unknown) < len(sizes):
        return 0

    if len(damaged_or_unknown) < sum(sizes):
        return 0

    if conditions == "?" and len(sizes) == 1:
        if sizes[0] == 1:
            return 1
        else:
            return 0

    # print(f"{conditions=} {sizes=}")

    cache_key = f"{conditions} {", ".join(str(s) for s in sizes)}"

    if cache_key in cache:
        return cache[cache_key]

    # Branch down two paths:
    #   1. We set the first unknown index to damaged
    #   2. We set the first unknown index to undamaged

    first_index_damaged = list(conditions)
    first_index_damaged[unknown_indices[0]] = "#"

    first_index_undamaged = list(conditions)
    first_index_undamaged[unknown_indices[0]] = "."

    solutions = 0

    solutions += count_solutions_in_branch("".join(first_index_damaged), sizes, cache)

    solutions += count_solutions_in_branch("".join(first_index_undamaged), sizes, cache)

    cache[cache_key] = solutions

    return solutions


def part1(lines: list[str]) -> Optional[int]:
    result = 0

    for conditions, sizes in parse_input(lines):
        result += count_solutions(conditions, sizes)

    return result


def part2(lines: list[str]) -> Optional[int]:
    result = 0

    i = 1
    for conditions, sizes in parse_input(lines, unfolding_factor=5):
        # print(f"{i}. {conditions} {", ".join(str(s) for s in sizes)}")
        i += 1
        result += count_solutions(conditions, sizes)

    return result


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
