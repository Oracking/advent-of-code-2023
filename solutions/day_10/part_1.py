from typing import List
from utils.grid import Grid, Point
from solutions.day_10.pipe_utils import Pipe


def part_1(lines: List[str]):
    grid_content = []
    starting_pipe_coordinate = None
    for y, row in enumerate(lines):
        grid_row = []
        for x, value in enumerate(row):
            grid_row.append(
                Pipe.create_pipe_from_string(value, Point(x, y))
            )
            if value == "S":
                starting_pipe_coordinate = Point(x, y)
        grid_content.append(grid_row)
    pipe_grid: Grid[Pipe] = Grid(grid_content)
    connect_pipes_together(pipe_grid)
    loop_length = find_loop_length(starting_pipe_coordinate, pipe_grid)
    return (loop_length + 1) // 2


def connect_pipes_together(pipe_grid: Grid[Pipe]):
    current_point = Point(0, 0)
    while current_point is not None:
        pipe = pipe_grid.get_value(current_point)
        for possible_connecting_point in pipe.possible_connecting_points:
            if pipe_grid.is_valid_coordinate(possible_connecting_point):
                connected_pipe = pipe_grid.get_value(possible_connecting_point)
                Pipe.connect_pipes(pipe, connected_pipe)
        current_point = pipe_grid.get_next_point_per_reading_flow(current_point)


def find_loop_length(starting_pipe_coordinate: Point, pipe_grid: Grid[Pipe]):
    starting_pipe = pipe_grid.get_value(starting_pipe_coordinate)
    loop_length = 0
    for starting_connected_pipe in starting_pipe.connected_pipes:
        previous_pipe = starting_pipe
        current_pipe = starting_connected_pipe
        loop_length = 0
        while current_pipe is not None:
            if current_pipe.is_starting_pipe:
                break
            next_current_pipe = current_pipe.get_next_pipe(previous_pipe)
            previous_pipe = current_pipe
            current_pipe = next_current_pipe
            loop_length += 1
    return loop_length
