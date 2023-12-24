from datetime import datetime
from math import floor
import sys
from enum import Enum
from functools import cached_property
from typing import Callable, Iterator, Optional

type Point = tuple[int, int]

X = 0
Y = 1


class Rock(Enum):
    ROUND = 1
    CUBE = 2


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


class PointSet:
    def __init__(self, points: Iterator[Point]):
        self.by_row: dict[int, set[int]] = {}
        self.by_column: dict[int, set[int]] = {}

        for p in points:
            self.add(p)

    def __iter__(self):
        return self._list().__iter__()

    def _list(self) -> list[tuple[int, int]]:
        l = []
        for y in self.by_row:
            for x in self.by_row[y]:
                l.append((x, y))
        return l

    def add(self, p: Point) -> None:
        x, y = p

        if y not in self.by_row:
            self.by_row[y] = set()
        self.by_row[y].add(x)

        if x not in self.by_column:
            self.by_column[x] = set()
        self.by_column[x].add(y)

    def remove(self, p: Point) -> None:
        x, y = p
        self.by_row[y].remove(x)
        self.by_column[x].remove(y)

    def find_closest(
        self,
        x=None,
        y=None,
        x_less_than=None,
        y_less_than=None,
        x_greater_than=None,
        y_greater_than=None,
    ) -> Optional[Point]:
        if x is not None:
            assert y is None, "can't supply both x and y"

            if y_less_than is not None:
                assert (
                    y_greater_than is None
                ), "can't supply y_less_than and y_greater_than"
                points = sorted(self.column(x))
                closest: Optional[Point] = None
                for p in points:
                    if p[Y] >= y_less_than:
                        return closest
                    closest = p
                return closest

            if y_greater_than is not None:
                points = reversed(sorted(self.column(x)))
                closest: Optional[Point] = None
                for p in points:
                    if p[Y] <= y_greater_than:
                        return closest
                    closest = p
                return closest

        if y is not None:
            if x_less_than is not None:
                assert (
                    x_greater_than is None
                ), "can't supply x_less_than and x_greater_than"
                points = sorted(self.row(y))
                closest: Optional[Point] = None
                for p in points:
                    if p[X] >= x_less_than:
                        return closest
                    closest = p
                return closest

            if x_greater_than is not None:
                points = reversed(sorted(self.row(Y)))
                closest: Optional[Point] = None
                for p in points:
                    if p[X] <= x_greater_than:
                        return closest
                    closest = p
                return closest

        assert False, "invalid find_closest call"

    def column(self, x: int) -> Iterator[tuple[int, int]]:
        if x in self.by_column:
            for y in self.by_column[x]:
                yield (x, y)

    def row(self, y: int) -> Iterator[tuple[int, int]]:
        if y in self.by_row:
            for x in self.by_row[y]:
                yield (x, y)


class Grid:
    def __init__(
        self,
        width: int,
        height: int,
        round_rocks: set[Point],
        cube_rocks: set[Point],
    ):
        self.width = width
        self.height = height
        self.round_rocks = PointSet(round_rocks)
        self.cube_rocks = PointSet(cube_rocks)
        self._moved_this_tilt: dict[Point, bool] = {}

    def __str__(self) -> str:
        result = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                c = "."
                if (x, y) in self.round_rocks:
                    c = "O"
                elif (x, y) in self.cube_rocks:
                    c = "#"
                row.append(c)
            result.append("".join(row))
        return "\n".join(result)

    def each_round_rock(self, tilt_dir: Direction) -> Iterator[Point]:
        """
        Moves through rocks in an order that means they will move
        _before_ any rocks that will collide with them. That means:
            - When tilting north, iterate top-to-bottom (row wise)
            - When tilting west, iterate left-to-right (column wise)
            - When tilting south, iterate bottom-to-top (row wise)
            - When tilting east, iterate right-to-left (column wise)
        """
        key: Callable[[Point], Point]

        match tilt_dir:
            case Direction.NORTH:
                # sort top-to-bottom
                key = lambda pos: (pos[1], pos[0])
            case Direction.WEST:
                # sort left-to-right
                key = lambda pos: (pos[0], pos[1])
            case Direction.SOUTH:
                # sort bottom-to-top
                key = lambda pos: (self.height - pos[1], pos[0])
            case Direction.EAST:
                # sort right-to-left
                key = lambda pos: (self.width - pos[0], pos[1])
            case _:
                assert False

        return sorted(self.round_rocks, key=key)

    def increment(self, p: Point, dir: Direction) -> Point:
        x, y = p
        match dir:
            case Direction.NORTH:
                return (x, y - 1)
            case Direction.WEST:
                return (x - 1, y)
            case Direction.SOUTH:
                return (x, y + 1)
            case Direction.EAST:
                return (x + 1, y)
            case _:
                assert False

    def load_on_north(self) -> int:
        return sum(self.height - y for _, y in self.round_rocks)

    def move_round_rock(self, pos: Point, tilt_dir: Direction) -> Point:
        """
        Moves the round rock located at the given position in the given
        tilt direction. Returns the final position.
        """

        def find_new_position() -> Point:
            if pos in self._moved_this_tilt:
                return pos

            x, y = pos

            next_round_rock: Optional[Point] = None
            next_cube_rock: Optional[Point] = None
            closest: Callable([Point, Point], Point)
            extreme_pos: Optional[Point] = None
            offset: (0, 0)

            match tilt_dir:
                case Direction.NORTH:
                    next_round_rock = self.round_rocks.find_closest(x=x, y_less_than=y)
                    next_cube_rock = self.cube_rocks.find_closest(x=x, y_less_than=y)
                    closest = lambda a, b: a if a[Y] > b[Y] else b
                    offset = (0, 1)
                    extreme_pos = (x, 0)
                case Direction.WEST:
                    next_round_rock = self.round_rocks.find_closest(y=y, x_less_than=x)
                    next_cube_rock = self.cube_rocks.find_closest(y=y, x_less_than=x)
                    closest = lambda a, b: a if a[X] > a[X] else b
                    offset = (1, 0)
                    extreme_pos = (0, y)
                case Direction.SOUTH:
                    next_round_rock = self.round_rocks.find_closest(
                        x=x, y_greater_than=y
                    )
                    next_cube_rock = self.cube_rocks.find_closest(x=x, y_greater_than=y)
                    closest = lambda a, b: a if a[Y] < b[Y] else b
                    extreme_pos = (x, self.height - 1)
                case Direction.EAST:
                    next_round_rock = self.round_rocks.find_closest(
                        y=y, x_greater_than=x
                    )
                    next_cube_rock = self.cube_rocks.find_closest(y=y, x_greater_than=x)
                    closest = lambda a, b: a if a[X] < b[X] else b
                    extreme_pos = (self.width - 1, y)
                case _:
                    assert False

            if next_round_rock is None and next_cube_rock is None:
                # No obstacles, so move to the extreme
                return extreme_pos

            if (
                next_round_rock is None
                or closest(next_round_rock, next_cube_rock) == next_cube_rock
            ):
                # This will hit a cube rock, offset it accordingly
                return tuple(map(sum, zip(next_cube_rock, offset)))

            # This will hit a round rock. Move _that_ rock place and offset this one
            next_round_rock = self.move_round_rock(next_round_rock, tilt_dir)
            return tuple(map(sum, zip(next_round_rock, offset)))

        new_pos = find_new_position()
        if new_pos != pos:
            self.round_rocks.remove(pos)
            self.round_rocks.add(new_pos)
            self._moved_this_tilt[new_pos] = True

        return new_pos

    def probe_from(self, pos: Point, dir: Direction):
        x, y = pos
        obstacles: Optional[set[Point]] = None

        match dir:
            case Direction.NORTH | Direction.SOUTH:
                # Obstacles in column
                obstacles = {
                    *self.cube_rocks.column(x),
                    *self.round_rocks.column(x),
                }

            case Direction.WEST | Direction.EAST:
                # Obstacles in row
                obstacles = {
                    *self.cube_rocks.row(y),
                    *self.round_rocks.row(y),
                }

            case _:
                assert False, f"Unexpected direction {repr(dir)}"

        while True:
            next_x, next_y = self.increment((x, y), dir)

            if next_x < 0 or next_y < 0:
                return (x, y)

            if next_x >= self.width or next_y >= self.height:
                return (x, y)

            if (next_x, next_y) in obstacles:
                return (x, y)

            x, y = (next_x, next_y)

    def tilt(self, tilt_dir: Direction) -> None:
        """
        Tilts the grid in the given direction.
        """
        self._moved_this_tilt = {}
        for x, y in self.each_round_rock(tilt_dir):
            new_x, new_y = self.probe_from((x, y), tilt_dir)
            if new_x != x or new_y != y:
                self.round_rocks.remove((x, y))
                self.round_rocks.add((new_x, new_y))

    @staticmethod
    def parse(lines: list[str]) -> "Grid":
        lines = (line.strip() for line in lines)
        lines = (line for line in lines if line != "")

        width = 0
        height = 0
        round_rocks: set[tuple[int, int]] = set()
        cube_rocks: set[tuple[int, int]] = set()

        for line in lines:
            if line == "":
                continue

            y = height
            height += 1
            assert width == 0 or width == len(line)
            width = len(line)

            for x, c in enumerate(line):
                match c:
                    case ".":
                        pass
                    case "#":
                        cube_rocks.add((x, y))
                    case "O":
                        round_rocks.add((x, y))
                    case _:
                        assert False

        assert height > 0
        assert width > 0

        return Grid(
            width=width, height=height, round_rocks=round_rocks, cube_rocks=cube_rocks
        )


def part1(lines: list[str]) -> Optional[int]:
    grid = Grid.parse(lines)
    grid.tilt(Direction.NORTH)
    return grid.load_on_north()


def part2(lines: list[str]) -> Optional[int]:
    grid = Grid.parse(lines)

    history: dict[str, int] = {}
    s: str = ""

    ITERATIONS = 1_000_000_000
    i = 0

    while i < ITERATIONS:
        print(f"{i=}")

        grid.tilt(Direction.NORTH)
        grid.tilt(Direction.WEST)
        grid.tilt(Direction.SOUTH)
        grid.tilt(Direction.EAST)

        s = str(grid)
        if s in history:
            # We have detected a loop. We can zoom i ahead however many full
            # loops will fit in what remains
            loop_size = i - history[s]
            remaining = ITERATIONS - i
            loops_we_can_do = floor(remaining / loop_size)
            i += loops_we_can_do * loop_size

        history[s] = i
        i += 1

    return grid.load_on_north()


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
