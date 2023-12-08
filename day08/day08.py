from math import floor, lcm, prod
import re
import sys
from typing import Iterable, Tuple


def infinite(seq, include_index=False):
    while True:
        for index, item in enumerate(seq):
            if include_index:
                yield (item, index)
            else:
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


def follow(dir: str, node: str, nodes: dict[str, (str, str)]) -> str:
    t = nodes[node]
    match dir:
        case "L":
            return t[0]
        case "R":
            return t[1]
        case _:
            assert False


def find_loop(
    from_node: str,
    instructions: Iterable[Tuple[str, int]],
    nodes: dict[str, (str, str)],
) -> (int, int):
    """
    Starts tracing a path a from_node and returns a tuple containing:
      - Start step
      - End step
      - Length
    """
    steps = 0
    node = from_node
    history = {}

    while True:
        dir, dir_index = instructions.__next__()
        node = follow(dir, node, nodes)
        steps += 1

        key = (node, dir_index)
        if key not in history:
            history[key] = []

        # if we have seen this combo before, we now know the loop start and length
        if len(history[key]) == 1:
            loop_start = history[key][0]
            loop_end = steps - 1
            loop_length = (loop_end - loop_start) + 1
            return (loop_start, loop_end, loop_length)

        history[key].append(steps)


def traverse_like_a_camel(instructions: str, nodes: dict[str, (str, str)]) -> int:
    node = "AAA"
    instructions = infinite(instructions)
    count = 0

    while node != "ZZZ":
        count += 1
        dir = instructions.__next__()
        node = follow(dir, node, nodes)

    return count


def traverse_like_a_ghost(instructions: str, nodes: dict[str, (str, str)]) -> int:
    initial_nodes = [node for node in nodes.keys() if node[-1] == "A"]

    loops = [
        find_loop(node, infinite(instructions, include_index=True), nodes)
        for node in initial_nodes
    ]

    assert len(loops) > 0

    loop_lengths = [loop_length for _, _, loop_length in loops]

    return lcm(*loop_lengths)


def part1(lines: list[str]) -> int:
    instructions, nodes = parse_input(lines)
    return traverse_like_a_camel(instructions, nodes)


def part2(lines):
    instructions, nodes = parse_input(lines)
    return traverse_like_a_ghost(instructions, nodes)


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
