import re
import sys
from typing import Optional


def parse_input(lines) -> (list[int], list[int]):
    times: Optional[list[int]] = None
    distances: Optional[list[int]] = None

    for line in lines:
        m = re.match(r"(.+):(.+)", line)
        if not m:
            continue

        values = [int(value) for value in re.split(r"\s+", m.group(2)) if value != ""]

        match m.group(1):
            case "Time":
                times = values
            case "Distance":
                distances = values
            case _:
                assert False, "Invalid "

    assert times is not None
    assert distances is not None
    assert len(times) == len(distances)

    return (times, distances)


def part1(lines):
    (times, distances) = parse_input(lines)

    # distance = (time - charge_time) * charge_time

    ways_to_win = []

    for time, target_distance in zip(times, distances):
        count = 0
        for charge_time in range(1, time):
            distance = (time - charge_time) * charge_time
            if distance > target_distance:
                count += 1
        ways_to_win.append(count)

    assert len(ways_to_win) > 0

    result = 1
    for ways in ways_to_win:
        result *= ways

    return result


def part2(lines):
    pass


if __name__ == "__main__":
    lines = (line.strip() for line in sys.stdin)
    lines = [line for line in lines if line != ""]
    print(part1(lines))
    print(part2(lines))
