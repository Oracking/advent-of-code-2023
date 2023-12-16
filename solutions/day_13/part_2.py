from typing import List, Tuple


def part_2(lines: List[str]):

    row_wise_grids: List[Tuple[str]] = []
    current_grid: List[str] = []
    for line in lines:
        if len(line) == 0 and len(current_grid) > 0:
            row_wise_grids.append(tuple(current_grid))
            current_grid = []
        else:
            current_grid.append(line)
    if len(current_grid) != 0:
        row_wise_grids.append(tuple(current_grid))

    column_wise_grids: List[Tuple[str]] = []
    for grid in row_wise_grids:
        column_wise_grids.append(convert_row_wise_grid_to_column_wise(grid))

    sum_columns_to_left = 0
    sum_rows_above = 0
    for row_wise_grid, column_wise_grid in zip(row_wise_grids, column_wise_grids):
        row_reflection_index = find_alternate_reflection_indexes(row_wise_grid)
        column_reflection_index = find_alternate_reflection_indexes(column_wise_grid)
        if row_reflection_index != len(row_wise_grid) - 1:
            sum_rows_above += row_reflection_index + 1
        elif column_reflection_index != len(column_wise_grid) - 1:
            sum_columns_to_left += column_reflection_index + 1

    return sum_columns_to_left + 100 * sum_rows_above


def convert_row_wise_grid_to_column_wise(row_wise_grid: Tuple[str]) -> Tuple[str]:
    column_wise_grid = []

    row_length = len(row_wise_grid[0])
    column_length = len(row_wise_grid)
    for row_index in range(row_length):
        column = []
        for column_index in range(column_length):
            column.append(row_wise_grid[column_index][row_index])
        column_wise_grid.append("".join(column))
    return tuple(column_wise_grid)


def find_reflection_point(grid: Tuple[str]) -> int:
    max_reflection_size = 0
    reflection_index = len(grid) - 1
    for index in range(len(grid)):
        min_size = min(index + 1, len(grid) - (index + 1))
        left_side = grid[index+1-min_size:index+1]
        right_side = grid[index+1: index+1+min_size][::-1]
        if left_side == right_side and min_size > max_reflection_size:
            reflection_index = index
            max_reflection_size = min_size
    return reflection_index


def find_alternate_reflection_indexes(grid: Tuple[str]) -> int:
    max_reflection_size = 0
    reflection_index = len(grid) - 1
    for index in range(len(grid)):
        min_size = min(index + 1, len(grid) - (index + 1))
        left_side = grid[index+1-min_size:index+1]
        right_side = grid[index+1: index+1+min_size][::-1]
        if compute_difference(left_side, right_side) == 1 and min_size > max_reflection_size:
            reflection_index = index
            max_reflection_size = min_size
    return reflection_index


def compute_difference(grid_1: Tuple[str], grid_2: Tuple[str]) -> int:
    difference = 0
    for row_1, row_2 in zip(grid_1, grid_2):
        for item_1, item_2 in zip(row_1, row_2):
            if item_1 != item_2:
                difference += 1
    return difference
