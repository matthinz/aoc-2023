from functools import reduce
import sys
from enum import Enum
from typing import Callable, Iterator, Literal, Optional

type Op = Literal["-"] | Literal["="]


def hash(input: str) -> int:
    result = 0
    for c in input:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def parse_input(lines: Iterator[str]) -> Iterator[tuple[str, Op, Optional[int]]]:
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if line != "")
    for line in lines:
        for token in line.split(","):
            if token == "":
                continue
            elif token.endswith("-"):
                yield (token[0:-1], "-", None)
            else:
                assert "=" in token
                label, focal_length = token.split("=")
                yield (label, "=", int(focal_length))


def part1(lines: list[str]) -> Optional[int]:
    return sum(
        hash(f"{label}{op}{'' if focal_length is None else str(focal_length)}")
        for label, op, focal_length in parse_input(lines)
    )


def part2(lines: list[str]) -> Optional[int]:
    boxes: list[Optional[list[tuple[str, int]]]] = [None] * 256
    for label, op, focal_length in parse_input(lines):
        box = hash(label)

        match op:
            case "-":
                # Remove the lens with given label
                if boxes[box] is not None:
                    boxes[box] = [(l, f) for l, f in boxes[box] if l != label]
            case "=":
                boxes[box] = boxes[box] or []

                lens_replaced = False
                for i, slot in enumerate(boxes[box]):
                    if slot[0] == label:
                        # Replace it
                        boxes[box][i] = (label, focal_length)
                        lens_replaced = True
                        break

                if not lens_replaced:
                    # add lens to the box
                    boxes[box].append((label, focal_length))

            case _:
                assert False

    focusing_power = 0

    for i, box in enumerate(boxes):
        if box is None:
            continue

        for j, l in enumerate(box):
            _, focal_length = l
            focusing_power += (i + 1) * (j + 1) * focal_length

    return focusing_power


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
