from math import floor
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


def count_ways_to_win_naive(times, distances):
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


def count_ways_to_win_with_math(target_time, target_distance):
    # distance = (target_time - charge_time) * charge_time
    # y = (t - x) * x
    # y = -x^2 + tx
    # dx/dy = -2x + t
    # 0 = -2x + t
    # -t = -2x
    # x = t/2 <-- this is where the slope hits zero, we can probe whole numbers around here?

    # to make this faster, do a binary search to find the upper and lower bounds?

    ways_to_win = 0

    charge_time = floor(target_time / 2)

    for i in range(0, target_time):
        lower = charge_time - i
        upper = charge_time + i

        lower_wins = False
        upper_wins = False

        if lower > 0:
            lower_distance = (target_time - lower) * lower
            lower_wins = lower_distance > target_distance
            if lower_wins:
                ways_to_win += 1

        if upper != lower:
            upper_distance = (target_time - upper) * upper
            upper_wins = upper_distance > target_distance

            if upper_wins:
                ways_to_win += 1

        if not (lower_wins or upper_wins):
            break

    return ways_to_win


def product(things):
    result = 0

    for x in things:
        result = (result or 1) * x

    return result


def part1(lines):
    (times, distances) = parse_input(lines)
    return product(
        count_ways_to_win_with_math(time, distance)
        for time, distance in zip(times, distances)
    )


def part2(lines):
    (times, distances) = parse_input(lines)
    time = int("".join(str(t) for t in times))
    distance = int("".join(str(d) for d in distances))
    return count_ways_to_win_with_math(time, distance)


if __name__ == "__main__":
    lines = (line.strip() for line in sys.stdin)
    lines = [line for line in lines if line != ""]
    print(part1(lines))
    print(part2(lines))
