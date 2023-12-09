import re
import sys
from typing import Iterable, Optional


def get_next_value(seq: list[int]) -> int:
    diffs: list[int] = []
    seq = list(seq)
    diffs_all_zero = True

    for i in range(0, len(seq) - 1):
        x = seq[i]
        y = seq[i + 1]
        diff = y - x
        diffs_all_zero = diffs_all_zero and diff == 0
        diffs.append(diff)

    # If the diffs are all 0, then the next value for seq is the same as
    # the last value
    if diffs_all_zero:
        return seq[-1]

    # Otherwise, we need to get the next value in the diff sequence
    # and add that to the last value
    next_diff = get_next_value(diffs)
    return seq[-1] + next_diff


def part1(lines: list[str]) -> Iterable[int]:
    next_values: list[int] = []

    for line in lines:
        line = re.sub(r"\s+", " ", line.strip())
        if line == "":
            continue

        raw_values = line.split(" ")
        next_values.append(get_next_value(int(value) for value in raw_values))

    return sum(next_values)


def part2(lines) -> Optional[int]:
    return None


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
