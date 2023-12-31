import re
import sys


def parse_round(desc):
    result = {}
    for s in desc.split(","):
        m = re.match(r"^\s*(\d+)\s+(\w+)\s*$", s)
        if m:
            result[m.group(2)] = int(m.group(1))
    return result


def parse_game(desc):
    m = re.match(r"^Game (\d+): (.+)", desc.strip())
    if not m:
        return

    id = int(m.group(1))
    rounds = (parse_round(round) for round in m.group(2).split(";"))

    return {"id": id, "rounds": list(rounds)}


def round_is_possible(round, maxes):
    for color in maxes:
        if color not in round:
            continue
        if round[color] > maxes[color]:
            return False
    return True


def game_is_possible(game, maxes):
    return all(round_is_possible(round, maxes) for round in game["rounds"])


def min_cubes_required(game):
    maxes = {}
    for round in game["rounds"]:
        for color in round:
            if color in maxes and round[color] > maxes[color]:
                maxes[color] = round[color]
            elif color not in maxes:
                maxes[color] = round[color]

    return maxes


def power(game):
    cubes = min_cubes_required(game)
    result = None
    for color in cubes:
        if result is None:
            result = cubes[color]
        else:
            result *= cubes[color]
    return result


def part1(lines):
    games = (parse_game(line) for line in lines if line)
    maxes = {"red": 12, "green": 13, "blue": 14}

    possible_games = (game for game in games if game_is_possible(game, maxes))

    return sum(game["id"] for game in possible_games)


def part2(lines):
    games = [parse_game(line) for line in lines if line]
    powers = [power(game) for game in games]
    return sum(powers)


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
