from collections import namedtuple
from typing import List, TypeVar, Generic, Iterable

Point = namedtuple("Point", ("x", "y"))

T = TypeVar('T')


class Grid(Generic[T]):
    def __init__(self, grid_content: List[List[T]]):
        self.min_x: int = 0
        self.min_y: int = 0
        self.max_y: int = len(grid_content) - 1
        self.max_x: int = len(grid_content[0]) - 1
        self.grid_content: List[List[T]] = grid_content

    def get_all_neighbours(self, point: Point, filter_for_valid: bool = True) -> List[Point]:
        return (self.get_vertical_neighbours(point, filter_for_valid)
                + self.get_diagonal_neighbours(point, filter_for_valid))

    def get_vertical_neighbours(self, point: Point, filter_for_valid: bool = True) -> List[Point]:
        x, y = point
        neighbours = [
            Point(x-1, y),
            Point(x, y-1),
            Point(x+1, y),
            Point(x, y + 1),
        ]
        return self.filter_for_valid_points(neighbours) if filter_for_valid else neighbours

    def get_diagonal_neighbours(self, point: Point, filter_for_valid: bool = True) -> List[Point]:
        x, y = point
        neighbours = [
            Point(x - 1, y - 1),
            Point(x + 1, y - 1),
            Point(x + 1, y + 1),
            Point(x - 1, y + 1)
        ]
        return self.filter_for_valid_points(neighbours) if filter_for_valid else neighbours

    def filter_for_valid_points(self, points: List[Point]) -> List[Point]:
        valid_points = []
        for point in points:
            if self.is_valid_coordinate(point):
                valid_points.append(point)
        return valid_points

    def is_valid_coordinate(self, point: Point) -> bool:
        return self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y

    def get_value(self, point: Point) -> T:
        return self.grid_content[point.y][point.x]

    def set_value(self, point: Point, value: T):
        self.grid_content[point.y][point.x] = value

    def get_row(self, y: int) -> List[T]:
        return self.grid_content[y]

    def get_rows_iter(self) -> Iterable[List[T]]:
        for row in self.grid_content:
            yield row

    def get_next_point_per_reading_flow(self, point: Point):
        if point.x == self.max_x:
            new_point = Point(0, point.y + 1)
        else:
            new_point = Point(point.x + 1, point.y)
        return new_point if self.is_valid_coordinate(new_point) else None

    def __repr__(self):
        return str(self)

    def __str__(self):
        representation = "[\n"
        for row in self.get_rows_iter():
            representation += f"{str(row)}\n"
        representation += "]\n"
        return representation

    def to_simple_hash(self):
        return "".join(["".join(row) for row in self.get_rows_iter()])