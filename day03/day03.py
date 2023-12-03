import sys


def is_symbol(c):
    if c == "\n":
        raise "should not be looking at newlines"
    return c != "." and not c.isdigit()


def touches_symbol(lines, x, y):
    for dy in (-1, 0, 1):
        if y + dy < 0 or y + dy >= len(lines):
            continue

        line = lines[y + dy]
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue

            if x + dx < 0 or x + dx >= len(line):
                continue

            if is_symbol(line[x + dx]):
                return True

    return False


def part1(lines):
    number_chars = []
    number_touches_symbol = False
    numbers = []

    def finish_number():
        nonlocal number_touches_symbol

        if len(number_chars) == 0:
            return

        if number_touches_symbol:
            number = int("".join(number_chars))
            numbers.append(number)

        number_chars.clear()
        number_touches_symbol = False

    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != ""]

    for line_index, line in enumerate(lines):
        for char_index, c in enumerate(line):
            match (c):
                case d if d.isdigit():
                    number_touches_symbol = number_touches_symbol or touches_symbol(
                        lines, char_index, line_index
                    )
                    number_chars.append(d)
                case _:
                    finish_number()

        finish_number()

    return sum(numbers)


def part2(lines):
    None


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
