import sys


class PartNumber:
    def __init__(self, number, x, y, adjacent_symbols=[]):
        self.number = number
        self.x = x
        self.y = y
        self.adjacent_symbols = adjacent_symbols


class Symbol:
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.adjacent_part_numbers = []

    def add_part_number(self, part_number):
        self.adjacent_part_numbers.append(part_number)

    def is_gear(self):
        return self.char == "*" and len(self.adjacent_part_numbers) == 2

    @staticmethod
    def is_symbol_char(c):
        if c == "\n":
            raise Exception("should not be looking at newlines")
        return c != "." and not c.isdigit()


class Schematic:
    def __init__(self):
        self.part_numbers = []
        self.symbols_by_position = {}

    def add_part_number(self, part_number):
        self.part_numbers.append(part_number)

    def add_symbol(self, char, x, y):
        pos = (x, y)
        existing = self.symbols_by_position.get(pos)
        if existing is not None:
            if existing.char == char:
                return existing
            else:
                raise Exception(f"Symbol already exists at {pos}")
        symbol = Symbol(char, x, y)
        self.symbols_by_position[pos] = symbol
        return symbol

    def symbol_at(self, x, y):
        self.symbols_by_position.get((x, y))

    def symbols(self):
        return self.symbols_by_position.values()

    @staticmethod
    def parse(lines):
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line != ""]

        schematic = Schematic()

        number_chars = []
        adjacent_symbols = set()
        number_start_x = None
        number_start_y = None

        def find_adjacent_symbols(x, y):
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue

                    symbol_x = x + dx
                    symbol_y = y + dy

                    if symbol_x < 0 or symbol_y < 0 or symbol_y >= len(lines):
                        continue

                    line = lines[symbol_y]

                    if symbol_x >= len(line):
                        continue

                    c = line[symbol_x]

                    if Symbol.is_symbol_char(c):
                        symbol = schematic.add_symbol(c, symbol_x, symbol_y)
                        adjacent_symbols.add(symbol)

        def finish_number():
            nonlocal number_start_x, number_start_y

            if len(number_chars) == 0:
                number_start_x = None
                number_start_y = None
                adjacent_symbols.clear()
                return

            if len(adjacent_symbols) == 0:
                number_start_x = None
                number_start_y = None
                number_chars.clear()
                return

            part_number = PartNumber(
                int("".join(number_chars)),
                number_start_x,
                number_start_y,
                adjacent_symbols,
            )

            for s in part_number.adjacent_symbols:
                s.add_part_number(part_number)

            schematic.add_part_number(part_number)

            number_chars.clear()
            adjacent_symbols.clear()
            number_start_x = None
            number_start_y = None

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                match (c):
                    case d if d.isdigit():
                        if len(number_chars) == 0:
                            number_start_x = x
                            number_start_y = y
                        number_chars.append(d)
                        find_adjacent_symbols(x, y)
                    case _:
                        finish_number()

            finish_number()

        return schematic


def part1(lines):
    schematic = Schematic.parse(lines)
    return sum(p.number for p in schematic.part_numbers)


def part2(lines):
    schematic = Schematic.parse(lines)

    gears = (s for s in schematic.symbols() if s.is_gear())

    gear_ratios = []
    for g in gears:
        ratio = 1
        for p in g.adjacent_part_numbers:
            ratio *= p.number
        gear_ratios.append(ratio)

    return sum(gear_ratios)


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
