from typing import List
from utils.grid import Grid, Point


def part_1(lines: List[str]):
    grid_content = [list(line) for line in lines]
    grid = Grid(grid_content)
    roll_up_balls(grid)
    return get_score(grid)


def roll_up_balls(grid):
    last_row_boundary = [-1] * (grid.max_x + 1)
    for y in range(0, grid.max_y + 1):
        for x in range(0, grid.max_x + 1):
            current_point = Point(x, y)
            if grid.get_value(current_point) == "#":
                last_row_boundary[x] = y
            elif grid.get_value(current_point) == "O":
                if y - last_row_boundary[x] > 1:
                    grid.set_value(current_point, ".")
                    grid.set_value(Point(x, last_row_boundary[x] + 1), "O")
                    last_row_boundary[x] += 1
                else:
                    last_row_boundary[x] = y


def get_score(grid):
    score = 0
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            if grid.get_value(Point(x, y)) == "O":
                score += (grid.max_y - y) + 1
    return score
