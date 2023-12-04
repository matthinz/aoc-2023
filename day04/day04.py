import sys


def part1(lines):
    lines = (line.strip() for line in lines)
    lines = [line for line in lines if line != ""]

    def parse_numbers(input):
        return set(int(value.strip()) for value in input.split(" ") if value != "")

    total_points = 0

    for line in lines:
        parts = line.partition(":")
        winners, numbers = parts[2].split("|")
        winners = parse_numbers(winners) & parse_numbers(numbers)
        point_value = 2 ** (len(winners) - 1) if len(winners) > 0 else 0
        total_points += point_value

    return total_points


def part2(lines):
    pass


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
