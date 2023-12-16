from typing import List, Set
import re
from utils.grid import Grid, Point


def part_1(lines: List[str]):
    grid_content = lines
    coordinates_in_scope_for_parsing: Set[Point] = set()
    grid = Grid([list(row) for row in grid_content])
    current_point = Point(0, 0)
    while current_point is not None:
        current_item = grid.get_value(current_point)
        if current_item != '.' and not current_item.isnumeric():
            neighbours = grid.get_all_neighbours(current_point)
            for neighbour in neighbours:
                if grid.get_value(neighbour).isnumeric():
                    coordinates_in_scope_for_parsing.add(neighbour)
        current_point = grid.get_next_point_per_reading_flow(current_point)

    part_numbers = []
    number_pattern = re.compile(r"\d+")
    for y_coord, row in enumerate(grid.get_rows_iter()):
        for number_match in number_pattern.finditer("".join(row)):
            for x_coord in range(number_match.span()[0], number_match.span()[1]):
                if Point(x_coord, y_coord) in coordinates_in_scope_for_parsing:
                    part_numbers.append(int(number_match.group(0)))
                    break
    return sum(part_numbers)
