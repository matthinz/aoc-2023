import re
import sys


def parse_card(spec):
    spec = re.sub(r"\s+", " ", spec).strip()
    m = re.match(r"Card (\d+): (.+)\|(.+)", spec)

    if m is None:
        raise Exception(f"Could not parse spec: #{repr(spec)}")

    card_index = int(m.group(1))
    winners = set(int(value.strip()) for value in m.group(2).split(" ") if value != "")
    numbers = set(int(value.strip()) for value in m.group(3).split(" ") if value != "")
    winning_number_count = len(winners & numbers)

    return (card_index, winning_number_count)


def part1(lines):
    lines = (line.strip() for line in lines)
    lines = [line for line in lines if line != ""]

    total_points = 0

    for line in lines:
        _, winning_number_count = parse_card(line)
        point_value = 2 ** (winning_number_count - 1) if winning_number_count > 0 else 0
        total_points += point_value

    return total_points


def part2(lines):
    lines = (line.strip() for line in lines)
    lines = [line for line in lines if line != ""]

    cards = [parse_card(line) for line in lines]
    counts = {}

    def count_for(card_index):
        if card_index in counts:
            return counts[card_index]

        _, winning_number_count = cards[card_index - 1]
        copies = cards[card_index : card_index + winning_number_count]

        count = 1

        for copy_index, _ in copies:
            count += count_for(copy_index)

        counts[card_index] = count

        return counts[card_index]

    return sum(count_for(card_index) for card_index, _ in cards)


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
