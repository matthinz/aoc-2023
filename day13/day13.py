import sys
from enum import Enum
from typing import Iterator, Optional


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


def parse_input(lines: list[str]) -> Iterator[list[str]]:
    lines = (line.strip() for line in lines)

    current: list[str] = []

    for line in lines:
        if line == "":
            if len(current) > 0:
                yield current
                current = []
        else:
            if len(current) > 0:
                assert len(line) == len(current[0])
            current.append(line)

    if len(current) > 0:
        yield current


def rows(grid: list[str]) -> Iterator[str]:
    for row in grid:
        yield row


def cols(grid: list[str]) -> Iterator[str]:
    i = 0
    while True:
        col: list[str] = []
        for row in grid:
            if i >= len(row):
                return
            col.append(row[i])
        yield col
        i += 1


def find_reflections(line: list[str]) -> Iterator[int]:
    """
    Finds points on <line> where a symmetry exists on the left and right sides.
    """
    for i in range(1, len(line)):
        symmetrical = True
        for j in range(0, i):
            left = i - j - 1
            right = i + j
            if left < 0 or right >= len(line):
                break

            if line[left] != line[right]:
                symmetrical = False
                break

        if symmetrical:
            yield i


def find_lines_of_reflection(lines: Iterator[str]) -> Iterator[int]:
    indices: Optional[set[int]] = None

    lines = list(lines)

    for pos, line in enumerate(lines):
        if indices is None:
            indices = set(i for i in range(0, len(line)))

        r = set(find_reflections(line))

        indices = indices & r

        if len(indices) == 0:
            break

    return indices or []


def find_lines_of_reflection_in_pattern(
    pattern: list[str],
) -> Iterator[tuple[int, Direction]]:
    for pos in find_lines_of_reflection(cols(pattern)):
        yield (pos, Direction.HORIZONTAL)

    for pos in find_lines_of_reflection(rows(pattern)):
        yield (pos, Direction.VERTICAL)


def find_variant_patterns(pattern: list[str]) -> Iterator[tuple[list[str], int, int]]:
    """
    Finds variants by smudging 1 cell at a time.
    """
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            # Yield a copy with (x,y) inverted
            new_c = "." if c == "#" else "#"
            new_row = row[:x] + new_c + row[x + 1 :]
            copy = pattern.copy()
            copy[y] = new_row
            yield copy, x, y


def score(line: int, dir: Direction) -> int:
    match dir:
        case Direction.VERTICAL:
            return line
        case Direction.HORIZONTAL:
            return 100 * line
        case _:
            assert False


def format_pattern(pattern: list[str], line: Optional[tuple[int, Direction]] = None):
    result = []

    for y, row in enumerate(pattern):
        if line is None:
            result.append(row)
        else:
            line_pos, line_dir = line
            if line_dir == Direction.HORIZONTAL:
                if len(result) == 0:
                    result.append("")
                if line_pos == y:
                    result.append(">" + ("-" * len(row)) + "<")
                result.append(f" {row} ")
                if y == len(pattern) - 1:
                    result.append("")
            elif line_dir == Direction.VERTICAL:
                if len(result) == 0:
                    result.append((" " * line_pos) + "v")
                result.append(row[:line_pos] + "|" + row[line_pos:])
                if y == len(pattern) - 1:
                    result.append((" " * line_pos) + "^")

    if line:
        result.append(str(score(*line)))

    return "\n".join(result)


def format_change(
    pattern: list[str],
    variant_pattern: list[str],
    old_lines_of_reflection: set[tuple[int, Direction]],
    variant_lines_of_reflection: set[tuple[int, Direction]],
) -> str:
    def split_and_pad(value: str) -> list[str]:
        lines = value.split("\n")
        max_len = max(len(line) for line in lines)
        return [line + (" " * (max_len - len(line))) for line in lines]

    assert len(old_lines_of_reflection) == 1
    assert len(variant_lines_of_reflection) == 1

    original = split_and_pad(format_pattern(pattern, list(old_lines_of_reflection)[0]))
    variant = split_and_pad(
        format_pattern(variant_pattern, list(variant_lines_of_reflection)[0])
    )

    while len(variant) < len(original):
        variant.append("")

    while len(original) < len(variant):
        original.append("")

    return "\n".join([f"{o}    {v}" for o, v in zip(original, variant)])


def part1(lines: list[str]) -> Optional[int]:
    result = 0

    for pattern in parse_input(lines):
        lines = list(find_lines_of_reflection_in_pattern(pattern))
        assert len(lines) == 1, f"wrong # of lines found ({len(lines)})"
        line, dir = lines[0]
        assert line
        result += score(line, dir)

    return result


def part2(lines: list[str]) -> Optional[int]:
    result = 0

    for pattern_index, pattern in enumerate(parse_input(lines)):
        old_lines_of_reflection = set(find_lines_of_reflection_in_pattern(pattern))
        assert (
            len(old_lines_of_reflection) == 1
        ), f"should have 1 old line of reflection (got {len(old_lines_of_reflection)})"

        found_variant = False
        variants_tried = 0
        prev_variant_pattern = None

        for variant_pattern, x, y in find_variant_patterns(pattern):
            if prev_variant_pattern is not None:
                assert "\n".join(prev_variant_pattern) != "\n".join(
                    pattern
                ), "variant does not differ"
            prev_variant_pattern = variant_pattern

            variants_tried += 1
            variant_lines_of_reflection = set(
                find_lines_of_reflection_in_pattern(variant_pattern)
            )

            if len(variant_lines_of_reflection) == 0:
                continue

            new_lines_of_reflection = (
                variant_lines_of_reflection - old_lines_of_reflection
            )

            match len(new_lines_of_reflection):
                case 0:
                    pass
                case 1:
                    new_line = list(new_lines_of_reflection)[0]
                    result += score(*new_line)
                    found_variant = True
                    break
                case _:
                    assert False, f"Too many new lines ({len(new_lines_of_reflection)})"

        assert (
            found_variant
        ), f"no variant found in #{pattern_index+1} (tried {variants_tried})"

    return result


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
