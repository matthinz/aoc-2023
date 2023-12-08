import re
import sys


def infinite(seq):
    while True:
        for item in seq:
            yield item


def parse_input(lines: list[str]) -> (str, dict[str, (str, str)]):
    instructions = None
    nodes: dict[str, (str, str)] = {}

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        if instructions is None:
            instructions = line
            continue

        m = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        assert m, f"{repr(line)} did not match"

        label = m.group(1)
        left = m.group(2)
        right = m.group(3)

        assert label not in nodes

        nodes[label] = (left, right)

    return (instructions, nodes)


def part1(lines: list[str]) -> int:
    instructions, nodes = parse_input(lines)

    node = "AAA"
    instructions = infinite(instructions)
    count = 0

    while node != "ZZZ":
        count += 1
        dir = instructions.__next__()
        t = nodes[node]
        match dir:
            case "L":
                node = t[0]
            case "R":
                node = t[1]
            case _:
                assert False

    return count


def part2(lines):
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
