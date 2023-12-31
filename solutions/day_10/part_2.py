from typing import List, Set
from utils.grid import Grid, Point
from solutions.day_10.pipe_utils import (
    Pipe, PIPE_STR_TO_Y_WEIGHT, NEIGHBOUR_DIFFS_TO_PIPE_STR
)


def part_2(lines: List[str]):
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
    loop_body_coordinates = find_loop_body_coordinates(starting_pipe_coordinate, pipe_grid)
    return calculate_bounded_area(pipe_grid, loop_body_coordinates)


def calculate_bounded_area(pipe_grid: Grid, loop_body_coordinates: Set[Point]) -> int:
    num_points_in_loop = 0
    for row_index, row in enumerate(pipe_grid.get_rows_iter()):
        in_loop = 0
        directional_switch_indicator = 0
        for index, pipe in enumerate(row):
            if pipe.point in loop_body_coordinates:
                directional_switch_indicator += PIPE_STR_TO_Y_WEIGHT[pipe.content]
                if abs(directional_switch_indicator) == 1:
                    in_loop = 1 - in_loop
                    directional_switch_indicator = 0
            elif in_loop:
                num_points_in_loop += 1
    return num_points_in_loop


def connect_pipes_together(pipe_grid: Grid[Pipe]):
    current_point = Point(0, 0)
    while current_point is not None:
        pipe = pipe_grid.get_value(current_point)
        for possible_connecting_point in pipe.possible_connecting_points:
            if pipe_grid.is_valid_coordinate(possible_connecting_point):
                connected_pipe = pipe_grid.get_value(possible_connecting_point)
                Pipe.connect_pipes(pipe, connected_pipe)
        current_point = pipe_grid.get_next_point_per_reading_flow(current_point)


def find_loop_body_coordinates(starting_pipe_coordinate: Point, pipe_grid: Grid[Pipe]) -> Set[Point]:
    starting_pipe = pipe_grid.get_value(starting_pipe_coordinate)
    loop_body_coordinates: Set[Point] = set()
    pipes_that_connect_to_starting_pipe = []
    for starting_connected_pipe in starting_pipe.connected_pipes:
        previous_pipe = starting_pipe
        current_pipe = starting_connected_pipe
        loop_body_coordinates = {starting_pipe.point}
        while current_pipe is not None:
            loop_body_coordinates.add(current_pipe.point)
            if current_pipe.is_starting_pipe:
                pipes_that_connect_to_starting_pipe = [starting_connected_pipe, previous_pipe]
                break
            next_current_pipe = current_pipe.get_next_pipe(previous_pipe)
            previous_pipe = current_pipe
            current_pipe = next_current_pipe

    starting_pipe_type = find_pipe_type_from_connected_pipes(
        starting_pipe.point,
        [pipe.point for pipe in pipes_that_connect_to_starting_pipe]
    )
    pipe_grid.set_value(
        starting_pipe.point,
        Pipe(starting_pipe_type, starting_pipe.point, [], True, False)
    )
    return loop_body_coordinates


def find_pipe_type_from_connected_pipes(pipe_coordinates: Point, connected_points: List[Point]) -> str:
    connected_diffs: List[Point] = []
    for connected_point in connected_points:
        connected_diffs.append(Point(
            connected_point.x - pipe_coordinates.x,
            connected_point.y - pipe_coordinates.y
        ))
    connected_diff_signatures = tuple(sorted(connected_diffs))
    return NEIGHBOUR_DIFFS_TO_PIPE_STR[connected_diff_signatures]
