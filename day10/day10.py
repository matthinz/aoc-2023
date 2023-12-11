import sys
from typing import Iterator, Optional
from enum import Enum


class NodeEdge(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


EDGES_BY_TILE: dict[str, set[NodeEdge]] = {
    "S": set(),
    "|": {NodeEdge.NORTH, NodeEdge.SOUTH},
    "-": {NodeEdge.WEST, NodeEdge.EAST},
    "L": {NodeEdge.NORTH, NodeEdge.EAST},
    "J": {NodeEdge.NORTH, NodeEdge.WEST},
    "7": {NodeEdge.WEST, NodeEdge.SOUTH},
    "F": {NodeEdge.SOUTH, NodeEdge.EAST},
}

TILES_BY_EDGE: dict[NodeEdge, list[str]] = {}
for tile in EDGES_BY_TILE:
    for edge in EDGES_BY_TILE[tile]:
        if edge not in TILES_BY_EDGE:
            TILES_BY_EDGE[edge] = []
        TILES_BY_EDGE[edge].append(tile)

OPPOSITE_EDGES: dict[NodeEdge, NodeEdge] = {
    NodeEdge.NORTH: NodeEdge.SOUTH,
    NodeEdge.EAST: NodeEdge.WEST,
    NodeEdge.SOUTH: NodeEdge.NORTH,
    NodeEdge.WEST: NodeEdge.EAST,
}


class Node:
    def __init__(self, c: str, x: int, y: int):
        self.c = c
        self.x = x
        self.y = y
        self.edges: dict[NodeEdge, Optional["Node"]] = {}

    def __repr__(self) -> str:
        return f"<{self.c} ({self.x},{self.y})>"

    def connect_to_neighbors(self, grid: list[list["Node"]]):
        """
        Connects this node on its edges.
        """
        for edge in EDGES_BY_TILE[self.c]:
            neighbor = self.find_neighbor(grid, edge)
            if neighbor is None:
                continue

            # If neighbor is compatible, that is it exposes the _opposite_ edge,
            # then make the connection.
            neighbor_edges = EDGES_BY_TILE[neighbor.c]
            if OPPOSITE_EDGES[edge] not in neighbor_edges:
                continue

            self.set_edge(edge, neighbor)

    def disconnect_from_neighbors(self):
        for edge in self.edges:
            n = self.edges[edge]
            if n is None:
                continue
            self.edges[edge] = None
            n.edges[OPPOSITE_EDGES[edge]] = None

    def find_neighbor(
        self, grid: list[list["Node"]], edge: NodeEdge
    ) -> Optional["Node"]:
        neighbor_x = self.x
        neighbor_y = self.y

        match edge:
            case NodeEdge.NORTH:
                neighbor_y -= 1
            case NodeEdge.EAST:
                neighbor_x += 1
            case NodeEdge.SOUTH:
                neighbor_y += 1
            case NodeEdge.WEST:
                neighbor_x -= 1

        if neighbor_y < 0 or neighbor_y >= len(grid):
            return

        row = grid[neighbor_y]

        if neighbor_x < 0 or neighbor_x >= len(row):
            return

        return row[neighbor_x]

    def get_edge(self, edge: NodeEdge) -> Optional["Node"]:
        if edge in self.edges:
            return self.edges[edge]

    def is_edge_set(self, edge: NodeEdge) -> bool:
        return bool(self.get_edge(edge))

    def guess_yourself(self, grid: list[list["Node"]]):
        neighbors = {
            NodeEdge.NORTH: self.find_neighbor(grid, NodeEdge.NORTH),
            NodeEdge.EAST: self.find_neighbor(grid, NodeEdge.EAST),
            NodeEdge.SOUTH: self.find_neighbor(grid, NodeEdge.SOUTH),
            NodeEdge.WEST: self.find_neighbor(grid, NodeEdge.WEST),
        }

        edges: set[NodeEdge] = set()

        for edge in neighbors:
            neighbor = neighbors[edge]
            if neighbor is None:
                continue

            neighbor_edges = EDGES_BY_TILE[neighbor.c]
            if OPPOSITE_EDGES[edge] in neighbor_edges:
                edges.add(edge)

        c = None
        for tile in EDGES_BY_TILE:
            has_all_edges = len(set(edges) & set(EDGES_BY_TILE[tile])) == len(edges)
            if has_all_edges:
                assert c is None, "multiple tiles matched"
                c = tile

        assert c, "no tile matched"
        self.c = c
        self.connect_to_neighbors(grid)

    def set_edge(self, edge: NodeEdge, node: Optional["Node"]) -> None:
        self.edges[edge] = node
        if node:
            node.edges[OPPOSITE_EDGES[edge]] = self


class NodeIterator:
    def __init__(self, node: Node):
        self.node = self.start_node = node
        self.entering_edge: Optional[NodeEdge] = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.entering_edge is None:
            self.entering_edge = [
                edge
                for edge in [
                    NodeEdge.NORTH,
                    NodeEdge.EAST,
                    NodeEdge.SOUTH,
                    NodeEdge.WEST,
                ]
                if self.node.is_edge_set(edge)
            ][0]
            assert self.entering_edge, "no starting edge found"
            return self.node

        for leaving_edge in EDGES_BY_TILE[self.node.c]:
            if leaving_edge == self.entering_edge:
                # this is the edge we entered on
                # we can't go backwards
                continue

            next_node = self.node.get_edge(leaving_edge)
            if next_node is None or next_node == self.start_node:
                raise StopIteration

            self.node = next_node
            self.entering_edge = OPPOSITE_EDGES[leaving_edge]

            return next_node


def parse_input(lines: list[str]) -> (Node, list[list[Node]]):
    grid = []
    start_node = None

    lines = (line for line in (line.strip() for line in lines) if line != "")

    # First pass: Build a 2d grid of nodes
    for y, line in enumerate(lines):
        row = []
        grid.append(row)

        for x, c in enumerate(line):
            if c == ".":
                row.append(None)
                continue

            node = Node(c, x, y)
            row.append(node)

            if c == "S":
                start_node = node

    assert start_node, "no start node found"

    # 2nd pass: Have each node connect itself to the others
    for row in grid:
        for node in row:
            if node and node != start_node:
                node.connect_to_neighbors(grid)

    # Finally, determine the start node's edges and determine its character
    start_node.guess_yourself(grid)

    return start_node, grid


def find_max_distance_from_start(start_node: Node) -> int:
    return len(set(NodeIterator(start_node))) // 2


def find_point_inside_loop(
    start_node: Node, grid: list[list[Node]]
) -> Optional[tuple[int, int]]:
    loop = set(NodeIterator(start_node))

    def is_inside_loop(point: (int, int)) -> bool:
        if node in loop:
            return False

        for dir in [NodeEdge.NORTH, NodeEdge.EAST, NodeEdge.SOUTH, NodeEdge.WEST]:
            hits = 0

            x, y = point

            while x > 0 and y >= 0 and y < len(grid):
                row = grid[y]
                if x >= len(row):
                    break
                n = row[x]
                if n in loop:
                    hits += 1
                x, y = move((x, y), dir)

            if hits % 2 == 0:
                return False

        return True

    # Find a point inside the grid where a ray traced out in each of the
    # cardinal directions hits the loop an odd number of times
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if is_inside_loop((x, y)):
                return (x, y)


def move(point: (int, int), dir: NodeEdge) -> (int, int):
    x, y = point
    match dir:
        case NodeEdge.NORTH:
            return (x, y - 1)
        case NodeEdge.EAST:
            return (x + 1, y)
        case NodeEdge.SOUTH:
            return (x, y + 1)
        case NodeEdge.WEST:
            return (x - 1, y)
        case _:
            assert False


def flood_fill(
    start: tuple[int, int],
    grid: list[list[Optional[Node]]],
) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    visited: set[tuple[int, int]] = set()
    to_visit: set[tuple[int, int]] = set([start])

    while len(to_visit) > 0:
        x, y = to_visit.pop()
        visited.add((x, y))

        node = grid[y][x]

        if node is not None:
            continue

        # This position is empty!
        result.add((x, y))

        # Evaluate nodes around us and see if we need to try and flood them
        for dir in [NodeEdge.NORTH, NodeEdge.EAST, NodeEdge.SOUTH, NodeEdge.WEST]:
            new_x, new_y = move((x, y), dir)

            if new_x < 0 or new_y < 0:
                continue

            if new_y >= len(grid):
                continue

            row = grid[new_y]
            if new_x >= len(row):
                continue

            if (new_x, new_y) in visited:
                continue

            to_visit.add((new_x, new_y))

    return result


def part1(lines: list[str]) -> int:
    start_node, _ = parse_input(lines)
    return find_max_distance_from_start(start_node)


def part2(lines) -> int:
    start_node, grid = parse_input(lines)

    def print_grid(
        grid: list[list[Node]], flooded_points: Optional[set[tuple[int, int]]] = None
    ):
        print("")
        for y, row in enumerate(grid):
            chars = []
            for x, node in enumerate(row):
                if flooded_points and (x, y) in flooded_points:
                    chars.append("*")
                elif node:
                    chars.append(node.c)
                else:
                    chars.append(".")
            print("".join(chars))
        print("")

    def clean_grid(grid: list[list[Node]]):
        loop = set(NodeIterator(start_node))
        for row in grid:
            for x, node in enumerate(row):
                if node is None:
                    continue

                if node in loop:
                    continue

                node.disconnect_from_neighbors()
                row[x] = None

    def expand_grid(grid: list[list[Node]]):
        expanded_grid = []
        for y, row in enumerate(grid):
            # Expand the row in the x direction
            expanded_row = []
            expanded_grid.append(expanded_row)
            for x, node in enumerate(row):
                expanded_row.append(node)

                if node is None or not node.is_edge_set(NodeEdge.EAST):
                    expanded_row.append(None)
                    continue

                # We're going to insert a - to maintain the connection
                east = node.get_edge(NodeEdge.EAST)
                connector = Node("-", x + 1, y)
                node.set_edge(NodeEdge.EAST, connector)
                east.set_edge(NodeEdge.WEST, connector)
                expanded_row.append(connector)

            # Expand the grid in the y direction
            new_row = []
            expanded_grid.append(new_row)
            for x, node in enumerate(expanded_row):
                if node is None or not node.is_edge_set(NodeEdge.SOUTH):
                    new_row.append(None)
                    continue

                south = node.get_edge(NodeEdge.SOUTH)
                connector = Node("|", x, y + 1)
                node.set_edge(NodeEdge.SOUTH, connector)
                south.set_edge(NodeEdge.NORTH, connector)
                new_row.append(connector)

        return expanded_grid

    clean_grid(grid)

    grid = expand_grid(grid)

    flood_start = find_point_inside_loop(start_node, grid)

    assert flood_start, "could not find point inside loop"

    flooded_points = flood_fill(flood_start, grid)

    # Since we expanded the grid, the odd rows/cols don't count
    return len(
        [point for point in flooded_points if point[0] % 2 == 0 and point[1] % 2 == 0]
    )

    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
