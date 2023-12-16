import re
from typing import List
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def set_x(self, new_x):
        self.x = new_x

    def set_y(self, new_y):
        self.y = new_y


def general_solution(lines: List[str], increment_factor: int):
    hashtag_pattern = re.compile("#")
    hashtag_indexes: List[Point] = []
    for y_index, row in enumerate(lines):
        hashtag_matches = hashtag_pattern.finditer(row)
        for match in hashtag_matches:
            hashtag_indexes.append(Point(match.span()[0], y_index))
    hashtag_indexes_sorted_by_x = hashtag_indexes[:]
    hashtag_indexes_sorted_by_y = hashtag_indexes[:]
    hashtag_indexes_sorted_by_x.sort(key=lambda point: point.x)
    hashtag_indexes_sorted_by_y.sort(key=lambda point: point.y)
    expand_along_coordinate(
        hashtag_indexes_sorted_by_x,
        lambda coords: coords.x,
        lambda coords, new_val: coords.set_x(new_val),
        increment_factor
    )
    expand_along_coordinate(
        hashtag_indexes_sorted_by_y,
        lambda coords: coords.y,
        lambda coords, new_val: coords.set_y(new_val),
        increment_factor
    )

    return find_sum_distances_between_every_pair(hashtag_indexes_sorted_by_x)


def expand_along_coordinate(
        coordinates_list: List[Point],
        coordinate_getter,
        coordinate_setter,
        increment_factor: int = 1
) -> List[Point]:
    previous_coordinate = coordinate_getter(coordinates_list[0])
    increment = 0
    for x_y_coordinates in coordinates_list:
        coordinate = coordinate_getter(x_y_coordinates)
        if coordinate - previous_coordinate > 1:
            increment += ((coordinate - previous_coordinate) - 1) * increment_factor
        previous_coordinate = coordinate
        coordinate_setter(x_y_coordinates, coordinate + increment)
    return coordinates_list


def find_sum_distances_between_every_pair(coordinates_list: List[Point]) -> int:
    sum_differences = 0
    for i, coordinates_1 in enumerate(coordinates_list):
        for coordinates_2 in coordinates_list[i:]:
            sum_differences += abs(coordinates_1.y - coordinates_2.y) + abs(coordinates_1.x - coordinates_2.x)
    return sum_differences
