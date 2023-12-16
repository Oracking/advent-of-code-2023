from typing import List, TypeVar
from utils.grid import Grid, Point


def part_2(lines: List[str]):
    grid_content = [list(line) for line in lines]
    grid = Grid(grid_content)
    cached_hashes = set()
    cached_hashes_list = []
    cached_scores = []
    directions = [Point(0, -1), Point(-1, 0), Point(0, 1), Point(1, 0)]
    for i in range(1000000000):
        for direction in directions:
            roll_in_direction(grid, direction)
        grid_hash = grid.to_simple_hash()
        if grid_hash in cached_hashes:
            loop_start = cached_hashes_list.index(grid_hash)
            return map_number_to_noose(cached_scores, loop_start, 1000000000)
        else:
            cached_hashes.add(grid_hash)
            cached_hashes_list.append(grid_hash)
            cached_scores.append(get_score(grid))


def roll_in_direction(grid: Grid, direction: Point):
    if direction == Point(0, -1):
        last_row_boundary = [-1] * (grid.max_x + 1)
        for y in range(0, grid.max_y + 1):
            for x in range(0, grid.max_x + 1):
                current_point = Point(x, y)
                if grid.get_value(current_point) == "#":
                    last_row_boundary[x] = y
                elif grid.get_value(current_point) == "O":
                    if y - last_row_boundary[x] > 1:
                        grid.set_value(current_point, "")
                        grid.set_value(Point(x, last_row_boundary[x] + 1), "O")
                        last_row_boundary[x] += 1
                    else:
                        last_row_boundary[x] = y

    elif direction == Point(0, 1):
        last_row_boundary = [grid.max_y + 1] * (grid.max_x + 1)
        for y in range(grid.max_y, -1, -1):
            for x in range(0, grid.max_x + 1):
                current_point = Point(x, y)
                if grid.get_value(current_point) == "#":
                    last_row_boundary[x] = y
                elif grid.get_value(current_point) == "O":
                    if abs(y - last_row_boundary[x]) > 1:
                        grid.set_value(current_point, "")
                        grid.set_value(Point(x, last_row_boundary[x] - 1), "O")
                        last_row_boundary[x] -= 1
                    else:
                        last_row_boundary[x] = y

    elif direction == Point(-1, 0):
        last_row_boundary = [-1] * (grid.max_y + 1)
        for x in range(0, grid.max_x + 1):
            for y in range(0, grid.max_y + 1):
                current_point = Point(x, y)
                if grid.get_value(current_point) == "#":
                    last_row_boundary[y] = x
                elif grid.get_value(current_point) == "O":
                    if abs(x - last_row_boundary[y]) > 1:
                        grid.set_value(current_point, "")
                        grid.set_value(Point(last_row_boundary[y] + 1, y), "O")
                        last_row_boundary[y] += 1
                    else:
                        last_row_boundary[y] = x

    elif direction == Point(1, 0):
        last_row_boundary = [grid.max_x + 1] * (grid.max_y + 1)
        for x in range(grid.max_x, -1, -1):
            for y in range(0, grid.max_y + 1):
                current_point = Point(x, y)
                if grid.get_value(current_point) == "#":
                    last_row_boundary[y] = x
                elif grid.get_value(current_point) == "O":
                    if abs(x - last_row_boundary[y]) > 1:
                        grid.set_value(current_point, "")
                        grid.set_value(Point(last_row_boundary[y] - 1, y), "O")
                        last_row_boundary[y] -= 1
                    else:
                        last_row_boundary[y] = x


T = TypeVar("T")


def map_number_to_noose(noose: List[T], loop_start: int, number: int) -> T:
    mapping_number = number - 1
    if mapping_number < loop_start:
        return noose[mapping_number]
    mapping_number = mapping_number - loop_start
    len_loop = len(noose) - loop_start
    return noose[(mapping_number % len_loop) + loop_start]


def get_score(grid):
    score = 0
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            if grid.get_value(Point(x, y)) == "O":
                score += (grid.max_y - y) + 1
    return score
