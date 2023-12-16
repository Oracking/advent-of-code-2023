from typing import List, Set, Dict, Tuple
import re
from utils.grid import Grid, Point


def part_2(lines: List[str]):
    grid_content = lines
    number_coord_to_gear_coord_map: Dict[Point, List[Point]] = {}
    grid = Grid([list(row) for row in grid_content])
    current_point = Point(0, 0)
    while current_point is not None:
        current_item = grid.get_value(current_point)
        if current_item == '*':
            neighbours = grid.get_all_neighbours(current_point)
            for neighbour in neighbours:
                if grid.get_value(neighbour).isnumeric():
                    gear_coords = number_coord_to_gear_coord_map.get(neighbour, [])
                    gear_coords.append(current_point)
                    number_coord_to_gear_coord_map[neighbour] = gear_coords
        current_point = grid.get_next_point_per_reading_flow(current_point)

    number_pattern = re.compile(r"\d+")
    gear_coords_to_number_spans: Dict[Point, Set[Tuple[Point, Point]]] = {}
    for y_coord, row in enumerate(grid.get_rows_iter()):
        for number_match in number_pattern.finditer("".join(row)):
            for x_coord in range(number_match.span()[0], number_match.span()[1]):
                number_point = Point(x_coord, y_coord)
                if number_point in number_coord_to_gear_coord_map:
                    for gear_coords in number_coord_to_gear_coord_map[number_point]:
                        numbers = gear_coords_to_number_spans.get(gear_coords, set())
                        numbers.add((Point(number_match.span()[0], y_coord), Point(number_match.span()[1], y_coord)))
                        gear_coords_to_number_spans[gear_coords] = numbers

    sum_of_gear_ratios = 0
    for number_spans in gear_coords_to_number_spans.values():
        if len(number_spans) == 2:
            ratio = 1
            for number_span in number_spans:
                ratio *= int("".join(grid.get_row(number_span[0].y)[number_span[0].x: number_span[1].x]))
            sum_of_gear_ratios += ratio
    return sum_of_gear_ratios
