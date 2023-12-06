from enum import Enum
import re
import sys
from typing import Optional


class MapEntry:
    def __init__(self, source: range, dest_offset: int) -> None:
        self._source: range = source
        self._dest_offset = dest_offset

    def map_source_to_dest(self, r: range) -> (range, range, range):
        """
        Maps source values to destination values.
        Returns a tuple of (unmapped_before, dest, unmapped_after):
        - unmapped_before: The set of values before the destination ones that weren't mapped
        - dest: The corresponding destination ranges
        - unmapped_after: The set of values after the destination range that weren't mapped
        """
        source = self.source()
        offset = self._dest_offset
        empty_range = range(0, 0)

        r_inside_source = r.start >= source.start and r.stop <= source.stop
        r_contains_source = r.start <= source.start and r.stop >= source.stop
        r_overlaps_left = (
            r.start < source.start and r.stop > source.start and r.stop <= source.stop
        )
        r_overlap_right = (
            r.start >= source.start and r.start < source.stop and r.stop >= source.stop
        )
        r_before = r.stop <= source.start
        r_after = r.start >= source.stop

        if r_inside_source:
            return (empty_range, range(r.start + offset, r.stop + offset), empty_range)
        elif r_contains_source:
            return (
                range(r.start, source.start),
                range(source.start + offset, source.stop + offset),
                range(source.stop, r.stop),
            )
        elif r_overlaps_left:
            return (
                range(r.start, source.start),
                range(source.start + offset, r.stop + offset),
                empty_range,
            )
        elif r_overlap_right:
            return (
                empty_range,
                range(r.start + offset, source.stop + offset),
                range(source.stop, r.stop),
            )
        elif r_before:
            return (r, empty_range, empty_range)
        elif r_after:
            return (empty_range, empty_range, r)
        else:
            assert False, "unhandled case"

    def source(self) -> range:
        return self._source

    def dest(self) -> range:
        return range(
            self._source.start + self._dest_offset,
            self._source.stop + self._dest_offset,
        )


class Map:
    """
    Map handles mapping source values to destination values
    """

    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination
        self.entries: list[MapEntry] = []

    def add(self, source_start: int, dest_start: int, length: int):
        self.entries.append(
            MapEntry(
                range(source_start, source_start + length),
                dest_start - source_start,
            )
        )

    def trace(self, ranges: list[range]) -> list[range]:
        """
        trace interprets ranges as a set of source values and returns the
        corresponding set of destination values
        """

        result: list[range] = []
        working_ranges = ranges.copy()

        while len(working_ranges) > 0:
            r = working_ranges.pop()

            if not r:
                continue

            unmapped_before: Optional[range] = None
            mapped: Optional[range] = None
            unmapped_after: Optional[range] = None

            for e in self.entries:
                t = e.map_source_to_dest(r)
                any_source_mapped = bool(t[1])

                if any_source_mapped:
                    unmapped_before, mapped, unmapped_after = t
                    break

            if mapped:
                result.append(mapped)
                working_ranges.append(unmapped_before)
                working_ranges.append(unmapped_after)
            else:
                result.append(r)

        return result


class Almanac:
    def __init__(self, seeds: list[range], maps: list[Map]):
        self.seeds: list[range] = seeds
        self.maps = maps

    def map_from(self, thing: str) -> Optional[Map]:
        for map in self.maps:
            if map.source == thing:
                return map

    def map_to(self, thing: str) -> Optional[Map]:
        for map in self.maps:
            if map.destination == thing:
                return map

    def min_location_for_seed(self, seed: range) -> int:
        map = self.map_from("seed")

        if not map:
            raise Exception("No seed map")

        locations = self.trace([seed], map)
        first_location = sorted(locations, key=lambda r: r.start)[0]
        return first_location.start

    def trace(self, ranges: list[range], map: Map) -> list[range]:
        next_ranges = map.trace(ranges)

        next_map = self.map_from(map.destination)
        if next_map:
            return self.trace(next_ranges, next_map)

        return next_ranges

    @staticmethod
    def parse(lines: list[str], seeds_as_ranges=True) -> "Almanac":
        lines = (line.strip() for line in lines)
        lines = [line for line in lines if line != ""]

        State = Enum("State", ["NEED_SEEDS", "READY_FOR_MAP", "IN_MAP"])

        seeds: list[range] = []
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
                    seeds.append(range(seed_start, seed_start + value))
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
            maps[-1].add(source_start, dest_start, length)

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
