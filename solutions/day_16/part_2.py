from typing import List, Tuple
from solutions.day_16.grid_object import GridObject
from utils.grid import Point, Grid


def part_2(lines: List[str]):
    grid_content: List[List[GridObject]] = []
    for y_index, line in enumerate(lines):
        row = []
        for x_index, object_type in enumerate(line):
            grid_object = GridObject(object_type, Point(x_index, y_index))
            row.append(grid_object)
        grid_content.append(row)

    grid = Grid(grid_content)
    max_energized = 0
    for y in range(0, grid.max_y+1):
        new_max_energized = max([
            get_num_energized([(Point(-1, y), Point(0, y))], grid),
            get_num_energized([(Point(grid.max_x + 1, y), Point(grid.max_x, y))], grid)
        ])
        max_energized = max([max_energized, new_max_energized])

    for x in range(0, grid.max_x+1):
        new_max_energized = max([
            get_num_energized([(Point(x, -1), Point(x, 0))], grid),
            get_num_energized([(Point(x, grid.max_y+1), Point(x, grid.max_y))], grid)
        ])
        max_energized = max([max_energized, new_max_energized])

    return max_energized


def get_num_energized(initial_beam_transition: List[Tuple[Point, Point]], grid: Grid):
    reset_grid_objects(grid)
    beam_transitions = initial_beam_transition
    while len(beam_transitions) > 0:
        next_beam_transitions: List[Tuple[Point, Point]] = []
        for from_coordinate, to_coordinate in beam_transitions:
            grid_object: GridObject = grid.get_value(to_coordinate)
            next_beam_coordinate = grid_object.get_next_beam_positions(from_coordinate)
            next_beam_coordinate = [coordinate for coordinate in next_beam_coordinate if
                                    grid.is_valid_coordinate(coordinate)]
            next_beam_transitions.extend([(grid_object.coordinate, coordinate) for coordinate in next_beam_coordinate])
        beam_transitions = next_beam_transitions

    next_point = Point(0, 0)
    num_energized_points = 0
    while next_point is not None:
        grid_object = grid.get_value(next_point)
        if grid_object.is_active:
            num_energized_points += 1
        next_point = grid.get_next_point_per_reading_flow(next_point)
    return num_energized_points


def reset_grid_objects(grid: Grid[GridObject]):
    next_point = Point(0, 0)
    while next_point is not None:
        grid.get_value(next_point).reset()
        next_point = grid.get_next_point_per_reading_flow(next_point)
