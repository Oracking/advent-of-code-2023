from typing import List
from collections import namedtuple
from utils.grid import Grid, Point
from heapq import heappush, heappop
from math import inf


Path = namedtuple("Path", ("heat_lost", "distance_from_end", "num_steps_in_current_direction", "visited"))


def part_2(lines: List[str]):
    grid_content = []
    for line in lines:
        row = [int(value) for value in list(line)]
        grid_content.append(row)
    grid = Grid(grid_content)
    return specialized_dijkstra(Point(0, 0), Point(grid.max_x, grid.max_y), grid)


def specialized_dijkstra(start_point: Point, end_point: Point, grid: Grid):
    cached_states = {}
    heap: List[Path] = [
        Path(
            0,
            euclidean_distance(start_point, end_point),
            0,
            (Point(-1, 0), start_point,)
        ),
        Path(
            0,
            euclidean_distance(start_point, end_point),
            0,
            (Point(0, -1), start_point,)
        )
    ]
    while len(heap) > 0:
        current_path = heappop(heap)
        if current_path.visited[-1] == end_point:
            return current_path.heat_lost

        current_pivot_point = current_path.visited[-1]
        current_direction = get_difference(current_path.visited[-2], current_path.visited[-1])

        neighbours = grid.get_vertical_neighbours(current_pivot_point)
        valid_neighbours = [neighbour for neighbour in neighbours if get_difference(current_pivot_point, neighbour) != Point(-current_direction.x, -current_direction.y)]
        if current_path.num_steps_in_current_direction < 4:
            valid_neighbours = [neighbour for neighbour in valid_neighbours if get_difference(current_pivot_point, neighbour) == current_direction]
        if current_path.num_steps_in_current_direction == 10:
            valid_neighbours = [neighbour for neighbour in valid_neighbours if
                                get_difference(current_pivot_point, neighbour) != current_direction]

        for neighbour in valid_neighbours:
            num_steps_in_current_direction = 1
            if get_difference(current_pivot_point, neighbour) == current_direction:
                num_steps_in_current_direction = current_path.num_steps_in_current_direction + 1

            new_path = Path(
                current_path.heat_lost + grid.get_value(neighbour),
                euclidean_distance(neighbour, end_point),
                num_steps_in_current_direction,
                (current_path.visited[-1], neighbour)
            )
            cached_state_key = (
                new_path.visited[-1],
                get_difference(new_path.visited[-2], new_path.visited[-1]),
                new_path.num_steps_in_current_direction
            )
            min_heat_loss = cached_states.get(cached_state_key, inf)
            if min_heat_loss > new_path.heat_lost:
                heappush(heap, new_path)
                cached_states[cached_state_key] = new_path.heat_lost
    return -1


def get_difference(point_1: Point, point_2: Point):
    return Point(point_2.x - point_1.x, point_2.y - point_1.y)


def euclidean_distance(point_1: Point, point_2: Point):
    return ((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2) ** 0.5
