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
                yield (token, token[0:-1], "-", None)
            else:
                assert "=" in token
                label, focal_length = token.split("=")
                yield (token, label, "=", int(focal_length))


def part1(lines: list[str]) -> Optional[int]:
    return sum(
        hash(f"{label}{op}{'' if focal_length is None else str(focal_length)}")
        for label, op, focal_length in parse_input(lines)
    )


def part2(lines: list[str]) -> Optional[int]:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
