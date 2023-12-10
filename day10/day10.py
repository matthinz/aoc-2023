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

        print(neighbors)

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
    def __init__(self, node: Node, entering_edge: NodeEdge):
        self.node = node
        self.entering_edge = entering_edge

    def __iter__(self):
        return self

    def __next__(self):
        for leaving_edge in EDGES_BY_TILE[self.node.c]:
            if leaving_edge == self.entering_edge:
                # this is the edge we entered on
                # we can't go backwards
                continue

            next_node = self.node.get_edge(leaving_edge)
            if next_node is None:
                raise StopIteration

            self.node = next_node
            self.entering_edge = OPPOSITE_EDGES[leaving_edge]

            return next_node


def parse_input(lines: list[str]) -> Node:
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

    return start_node


def find_max_distance_from_start(start_node: Node) -> int:
    print(start_node.edges)

    start_edge = [
        edge
        for edge in [
            NodeEdge.NORTH,
            NodeEdge.EAST,
            NodeEdge.SOUTH,
            NodeEdge.WEST,
        ]
        if start_node.is_edge_set(edge)
    ][0]

    assert start_edge, "no starting edge found"

    visited = {}
    for node in NodeIterator(start_node, start_edge):
        if node in visited:
            break
        visited[node] = True

    return len(visited) // 2


def part1(lines: list[str]) -> int:
    start_node = parse_input(lines)
    print((start_node.c, start_node.x, start_node.y))
    return find_max_distance_from_start(start_node)


def part2(lines) -> int:
    pass


if __name__ == "__main__":
    lines = [line for line in sys.stdin]
    print(part1(lines))
    print(part2(lines))
