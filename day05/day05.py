from enum import Enum
import re
import sys
from typing import Optional


class Range:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length


class Map:
    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination
        self.source_ranges: list[Range] = []
        self.destination_ranges: list[Range] = []

    def add_range(self, dest_start: int, source_start: int, length: int):
        self.source_ranges.append(Range(source_start, length))
        self.destination_ranges.append(Range(dest_start, length))

    def dest_for(self, source: int) -> int:
        for source_range, destination_range in zip(
            self.source_ranges, self.destination_ranges
        ):
            if (
                source >= source_range.start
                and source < source_range.start + source_range.length
            ):
                return destination_range.start + (source - source_range.start)

        return source


class Almanac:
    def __init__(self, seeds: list[Range], maps: list[Map]):
        self.seeds: list[Range] = seeds
        self.maps = maps
        pass

    def min_location_for_seed(self, seed: Range) -> int:
        best: Optional[int] = None

        for i in range(seed.start, seed.start + seed.length):
            thing = "seed"
            num = i

            while True:
                if thing == "location":
                    if best is None or num < best:
                        best = num
                    break

                map = self.map_from(thing)
                if not map:
                    raise Exception(f"No map found for source {thing}")

                num = map.dest_for(num)
                thing = map.destination

        return best

    def map_from(self, thing) -> Optional[Map]:
        for m in self.maps:
            if m.source == thing:
                return m

    @staticmethod
    def parse(lines: list[str], seeds_as_ranges=True) -> "Almanac":
        lines = (line.strip() for line in lines)
        lines = [line for line in lines if line != ""]

        State = Enum("State", ["NEED_SEEDS", "READY_FOR_MAP", "IN_MAP"])

        seeds: list[Range] = []
        maps: list[Map] = []
        state: State = State.NEED_SEEDS

        def parse_seeds():
            nonlocal seeds

            if line == "":
                return

            m = re.match(r"^seeds: (.+)", line)
            if not m:
                raise Exception("Need seeds but line doesn't look like seeds")

            values = [int(value) for value in m.group(1).split(" ")]

            if not seeds_as_ranges:
                # pretend each seed is a range with length 1
                values_with_ones = []
                for value in values:
                    values_with_ones.append(value)
                    values_with_ones.append(1)
                values = values_with_ones

            seed_start: Optional[int] = None

            for value in values:
                if seed_start is None:
                    seed_start = value
                else:
                    seeds.append(Range(seed_start, value))
                    seed_start = None

            return State.READY_FOR_MAP

        def start_map():
            if line == "":
                return

            m = re.match(r"(.+)-to-(.+) map:", line)
            if not m:
                raise Exception("Ready for map but didn't get one")

            source = m.group(1)
            destination = m.group(2)

            map = Map(source, destination)
            maps.append(map)

            return State.IN_MAP

        def continue_map():
            if line == "":
                return

            m = re.match(r"(.+)-to-(.+) map:", line)
            if m:
                return start_map()

            dest_start, source_start, length = (int(value) for value in line.split(" "))
            maps[-1].add_range(dest_start, source_start, length)

        for line in lines:
            match state:
                case State.NEED_SEEDS:
                    state = parse_seeds() or state

                case State.READY_FOR_MAP:
                    state = start_map() or state

                case State.IN_MAP:
                    state = continue_map() or state

        if seeds is None:
            raise Exception("No seeds found")

        return Almanac(seeds, maps)


def part1(lines):
    almanac = Almanac.parse(lines, seeds_as_ranges=False)
    return min(almanac.min_location_for_seed(seed) for seed in almanac.seeds)


def part2(lines):
    almanac = Almanac.parse(lines)
    return min(almanac.min_location_for_seed(seed) for seed in almanac.seeds)


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
