from enum import Enum
import re
import sys
from typing import Optional


class Map:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.ranges = []

    def add_range(self, dest_start: int, source_start: int, length: int):
        self.ranges.append((dest_start, source_start, length))

    def dest_for(self, source: int) -> int:
        for dest_start, source_start, length in self.ranges:
            if source >= source_start and source < source_start + length:
                return dest_start + (source - source_start)

        return source


class Almanac:
    def __init__(self, seeds: list[int], maps: list[Map]):
        self.seeds = seeds
        self.maps = maps
        pass

    def location_for_seed(self, seed):
        thing = "seed"
        num = seed

        while True:
            if thing == "location":
                return num

            map = self.map_from(thing)
            if not map:
                raise Exception(f"No map found for source {thing}")

            num = map.dest_for(num)
            thing = map.destination

    def map_from(self, thing) -> Optional[Map]:
        for m in self.maps:
            if m.source == thing:
                return m

    @staticmethod
    def parse(lines: list[str]) -> "Almanac":
        lines = (line.strip() for line in lines)
        lines = [line for line in lines if line != ""]

        State = Enum("State", ["NEED_SEEDS", "READY_FOR_MAP", "IN_MAP"])

        seeds: list[int] = []
        maps: list[Map] = []
        state: State = State.NEED_SEEDS

        def parse_seeds():
            nonlocal seeds

            if line == "":
                return

            m = re.match(r"^seeds: (.+)", line)
            if not m:
                raise Exception("Need seeds but line doesn't look like seeds")

            for seed in m.group(1).split(" "):
                seeds.append(int(seed))

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
    almanac = Almanac.parse(lines)
    return min(almanac.location_for_seed(seed) for seed in almanac.seeds)


def part2(lines):
    lines = (line.strip() for line in lines)
    lines = [line for line in lines if line != ""]


if __name__ == "__main__":
    input = list(sys.stdin)
    print(part1(input))
    print(part2(input))
