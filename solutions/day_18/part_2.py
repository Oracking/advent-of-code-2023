from typing import List, Dict, Iterable, Tuple, Union
import re
from utils.grid import Point
from solutions.day_10.pipe_utils import Pipe, NEIGHBOUR_DIFFS_TO_PIPE_STR, PIPE_STR_TO_Y_WEIGHT


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

DIRECTIONS_BY_INDEX = ["R", "D", "L", "U"]


def part_2(lines: List[str]):
    y_index_to_corner_pipes, perimeter_area = get_corner_pipes_grouped_by_y_coordinate(lines)
    return calculate_bounded_area(y_index_to_corner_pipes) + perimeter_area


def get_corner_pipes_grouped_by_y_coordinate(lines: List[str]) -> Tuple[Dict[int, List[Pipe]], int]:
    line_pattern = re.compile(r"(?P<direction>\w)\s(?P<amount>\d+)\s\(#(?P<colour>[\w\d]+)\)")
    loop_body_coordinates: List[Point] = [Point(0, 0)]
    y_index_to_corners_map: Dict[int, List[Pipe]] = {}
    perimeter_area = 0
    for line in lines:
        _, _, coded_instruction = line_pattern.match(line).groups()
        amount = int(coded_instruction[:5], 16)
        direction = DIRECTIONS_BY_INDEX[int(coded_instruction[-1])]
        perimeter_area += int(amount)
        direction_vector = DIRECTION_TO_VECTOR[direction]

        next_point = sum_points(loop_body_coordinates[-1], direction_vector)
        if len(loop_body_coordinates) > 2:
            set_pipe_type_at_index(
                [loop_body_coordinates[-2], loop_body_coordinates[-1], next_point],
                1,
                y_index_to_corners_map
            )
        last_point = sum_points(next_point, scalar_multiply(direction_vector, amount-1))
        loop_body_coordinates.append(last_point)

    loop_body_coordinates.pop(0)
    set_pipe_type_at_index(loop_body_coordinates, -1, y_index_to_corners_map)
    set_pipe_type_at_index(loop_body_coordinates, 0, y_index_to_corners_map)
    return y_index_to_corners_map, perimeter_area


def set_pipe_type_at_index(
        loop_body_coordinates: List[Point], index: int,
        y_index_to_corner_map: Dict[int, List[Pipe]]
) -> None:
    point = loop_body_coordinates[index]
    pipe_type = find_pipe_type_from_connected_pipes(
        point, [loop_body_coordinates[index-1], loop_body_coordinates[index+1]]
    )
    corners = y_index_to_corner_map.get(point.y, [])
    corners.append(Pipe.create_pipe_from_string(pipe_type, point))
    y_index_to_corner_map[point.y] = corners


def sum_points(point_1: Point, point_2: Point) -> Point:
    return Point(point_1.x + point_2.x, point_1.y + point_2.y)


def scalar_multiply(point: Point, scalar: int):
    return Point(point.x * scalar, point.y * scalar)


def get_unit_vector(point: Point):
    unit_scalar = (point.x ** 2 + point.y ** 2) ** 0.5
    if unit_scalar == 0:
        return point
    return Point(round(point.x // unit_scalar), round(point.y // unit_scalar))


def find_pipe_type_from_connected_pipes(pipe_coordinates: Point, connected_points: List[Point]) -> str:
    connected_diffs: List[Point] = []
    for connected_point in connected_points:
        connected_diffs.append(get_unit_vector(Point(
            connected_point.x - pipe_coordinates.x,
            connected_point.y - pipe_coordinates.y
        )))
    connected_diff_signatures = tuple(sorted(connected_diffs))
    return NEIGHBOUR_DIFFS_TO_PIPE_STR[connected_diff_signatures]


def generate_rows_with_corners(y_index_to_corners_map: Dict[int, List[Pipe]]) -> Iterable[Tuple[int, List[Pipe]]]:
    sorted_y_coordinates_with_corners = sorted(y_index_to_corners_map.keys())
    corners: List[Pipe] = []
    for y_coordinate_with_a_corner in sorted_y_coordinates_with_corners:
        current_corners = sorted(y_index_to_corners_map[y_coordinate_with_a_corner], key=lambda a_pipe: a_pipe.point.x)
        corners = merge_with_left_preference(current_corners, corners)
        yield y_coordinate_with_a_corner, corners

        next_corners = []
        for corner in corners:
            if corner.content == "F" or corner.content == "7" or corner.content == "|":
                next_corners.append(Pipe.create_pipe_from_string("|", Point(corner.point.x, corner.point.y + 1)))
        corners = next_corners

        next_y = y_coordinate_with_a_corner + 1
        if next_y not in y_index_to_corners_map:
            yield next_y, corners


def merge_with_left_preference(corners_1: List[Pipe], corners_2: List[Pipe]):
    i = 0
    j = 0
    merged_corners = []
    while not (i == len(corners_1) and j == len(corners_2)):
        if i == len(corners_1):
            merged_corners.append(corners_2[j])
            j += 1
        elif j == len(corners_2):
            merged_corners.append(corners_1[i])
            i += 1
        elif corners_1[i].point.x == corners_2[j].point.x:
            merged_corners.append(corners_1[i])
            i += 1
            j += 1
        elif corners_1[i].point.x < corners_2[j].point.x:
            merged_corners.append(corners_1[i])
            i += 1
        else:
            merged_corners.append(corners_2[j])
            j += 1
    return merged_corners


def calculate_bounded_area(y_index_to_corner_pipes: Dict[int, List[Pipe]]) -> int:
    total_area = 0
    area_of_previous_row = 0
    previous_row_index = 0
    for row_index, corners in generate_rows_with_corners(y_index_to_corner_pipes):
        total_area += area_of_previous_row * (row_index - previous_row_index - 1)
        area_of_row = calculate_area_of_row(corners)
        total_area += area_of_row
        previous_row_index = row_index
        area_of_previous_row = area_of_row
    return total_area


def calculate_area_of_row(corners_for_row: List[Pipe]) -> int:
    total_area = 0
    in_loop = 0
    directional_switch_indicator = 0
    previous_pipe: Union[Pipe, None] = None
    for index, pipe in enumerate(corners_for_row):
        if in_loop and directional_switch_indicator == 0:
            total_area += pipe.point.x - previous_pipe.point.x - 1
        directional_switch_indicator += PIPE_STR_TO_Y_WEIGHT[pipe.content]
        if abs(directional_switch_indicator) == 1:
            in_loop = 1 - in_loop
            directional_switch_indicator = 0
        previous_pipe = pipe
    return total_area