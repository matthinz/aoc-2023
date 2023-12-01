import functools
import sys
import re

ENGLISH_DIGITS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def replace_first_english_digit(line, english_digits):
    first_index = float("inf")
    to_replace = None

    for english_digit in english_digits:
        index = line.find(english_digit)
        if index >= 0 and index < first_index:
            first_index = index
            to_replace = english_digit

    if to_replace:
        replacement = str(english_digits.index(to_replace) + 1)
        parts = line.partition(to_replace)
        return parts[0] + replacement + parts[2]

    return line


def replace_last_english_digit(line, english_digits):
    last_index = float("-inf")
    to_replace = None

    for english_digit in english_digits:
        index = line.rfind(english_digit)
        if index >= 0 and index > last_index:
            last_index = index
            to_replace = english_digit

    if to_replace:
        replacement = str(english_digits.index(to_replace) + 1)
        parts = line.rpartition(to_replace)
        return parts[0] + replacement + parts[2]

    return line


def parse_calibration_value(line, english_digits=[]):
    line = line.strip()

    orig_line = line

    line = replace_first_english_digit(line, english_digits)
    line = replace_last_english_digit(line, english_digits)

    first_digit_regex = r"^[^\d]*(\d)"
    last_digit_regex = r"(\d)[^\d]*$"

    m = re.search(first_digit_regex, line)
    if m is None:
        return 0
    first_digit = m.group(1)

    m = re.search(last_digit_regex, line)
    if m is None:
        return 0

    last_digit = m.group(1)

    if line != orig_line:
        print(f"{orig_line} --> {line} -> {first_digit + last_digit}")

    return int(first_digit + last_digit)


def part1(input):
    return sum(map(parse_calibration_value, input))


def part2(input):
    return sum(
        map(
            functools.partial(parse_calibration_value, english_digits=ENGLISH_DIGITS),
            input,
        )
    )


input = list(sys.stdin)
print(part1(input))
print(part2(input))
