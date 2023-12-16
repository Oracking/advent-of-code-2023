from typing import List, Tuple
from solutions.day_16.grid_object import GridObject
from utils.grid import Point, Grid


def part_1(lines: List[str]):
    grid_content: List[List[GridObject]] = []
    for y_index, line in enumerate(lines):
        row = []
        for x_index, object_type in enumerate(line):
            grid_object = GridObject(object_type, Point(x_index, y_index))
            row.append(grid_object)
        grid_content.append(row)

    grid = Grid(grid_content)
    beam_transitions: List[Tuple[Point, Point]] = [(Point(-1, 0), Point(0, 0))]
    while len(beam_transitions) > 0:
        next_beam_transitions: List[Tuple[Point, Point]] = []
        for from_coordinate, to_coordinate in beam_transitions:
            grid_object = grid.get_value(to_coordinate)
            next_beam_coordinate = grid_object.get_next_beam_positions(from_coordinate)
            next_beam_coordinate = [coordinate for coordinate in next_beam_coordinate if grid.is_valid_coordinate(coordinate)]
            next_beam_transitions.extend([(grid_object.coordinate, coordinate) for coordinate in next_beam_coordinate])
        beam_transitions = next_beam_transitions

    next_point = Point(0, 0)
    num_energized_points = 0
    while next_point is not None:
        grid_object = grid.get_value(next_point)
        if grid_object.is_active:
            grid_object.object_type = "#"
            num_energized_points += 1
        next_point = grid.get_next_point_per_reading_flow(next_point)
    return num_energized_points