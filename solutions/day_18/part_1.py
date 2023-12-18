from typing import List
import re
from utils.grid import Grid, Point
from solutions.day_10.pipe_utils import Pipe
from solutions.day_10.part_2 import find_pipe_type_from_connected_pipes, calculate_bounded_area


DEFAULT_CANVAS_WIDTH = 1000


DIRECTION_TO_VECTOR = {
    "R": Point(1, 0),
    "L": Point(-1, 0),
    "U": Point(0, -1),
    "D": Point(0, 1)
}


DIRECTION_TO_FLAT_PIPE = {
    "R": "-",
    "L": "-",
    "U": "|",
    "D": "|"
}


def part_1(lines: List[str]):
    large_canvas = [["."] * DEFAULT_CANVAS_WIDTH for _ in range(DEFAULT_CANVAS_WIDTH)]
    canvas_grid: Grid[str] = Grid(large_canvas)
    pipe_coordinates = add_pipes_to_grid(lines, canvas_grid)
    pipe_grid: Grid[Pipe] = create_pipe_grid(canvas_grid)
    return len(pipe_coordinates) + calculate_bounded_area(pipe_grid, set(pipe_coordinates))


def create_pipe_grid(canvas_grid: Grid) -> Grid[Pipe]:
    pipe_grid_content = []
    for y, row in enumerate(canvas_grid.grid_content):
        grid_row = []
        for x, value in enumerate(row):
            grid_row.append(
                Pipe.create_pipe_from_string(value, Point(x, y))
            )
        pipe_grid_content.append(grid_row)
    return Grid(pipe_grid_content)


def add_pipes_to_grid(lines: List[str], canvas_grid: Grid) -> List[Point]:
    line_pattern = re.compile(r"(?P<direction>\w)\s(?P<amount>\d+)\s\(#(?P<colour>[\w\d]+)\)")
    loop_body_coordinates: List[Point] = [Point(DEFAULT_CANVAS_WIDTH // 2, DEFAULT_CANVAS_WIDTH // 2)]
    for line in lines:
        direction, amount, colour = line_pattern.match(line).groups()
        amount = int(amount)
        pipe_type = DIRECTION_TO_FLAT_PIPE[direction]
        direction_vector = DIRECTION_TO_VECTOR[direction]
        for i in range(amount):
            next_point = sum_points(loop_body_coordinates[-1], direction_vector)
            loop_body_coordinates.append(next_point)
            if i == 0 and len(loop_body_coordinates) > 2:
                set_pipe_type_at_index(loop_body_coordinates, -2, canvas_grid)
            canvas_grid.set_value(next_point, pipe_type)
    loop_body_coordinates.pop(0)
    set_pipe_type_at_index(loop_body_coordinates, -1, canvas_grid)
    set_pipe_type_at_index(loop_body_coordinates, 0, canvas_grid)
    return loop_body_coordinates


def set_pipe_type_at_index(loop_body_coordinates: List[Point], index: int, grid: Grid) -> None:
    pipe_type = find_pipe_type_from_connected_pipes(
        loop_body_coordinates[index], [loop_body_coordinates[index-1], loop_body_coordinates[index+1]]
    )
    grid.set_value(loop_body_coordinates[index], pipe_type)


def sum_points(point_1: Point, point_2: Point) -> Point:
    return Point(point_1.x + point_2.x, point_1.y + point_2.y)