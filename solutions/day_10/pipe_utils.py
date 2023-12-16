from typing import List, Dict
from utils.grid import Point

PIPE_STR_TO_Y_WEIGHT: Dict[str, int] = {
    "|": 1,
    "-": 0,
    "L": -0.5,
    "J": 0.5,
    "7": -0.5,
    "F": 0.5,
    "S": None,
    ".": 0
}


PIPE_STR_TO_VALID_NEIGHBOUR_DIFF: Dict[str, List[Point]] = {
    "|": [Point(0, -1), Point(0, 1)],
    "-": [Point(-1, 0), Point(1, 0)],
    "L": [Point(0, -1), Point(1, 0)],
    "J": [Point(0, -1), Point(-1, 0)],
    "7": [Point(0, 1), Point(-1, 0)],
    "F": [Point(0, 1), Point(1, 0)],
    "S": [Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 0)],
    ".": []
}


class Pipe:
    def __init__(self, content: str, point: Point, possible_connecting_points: List[Point], is_starting_pipe: bool, is_dud: bool):
        self.content = content
        self.is_starting_pipe = is_starting_pipe
        self.is_dud = is_dud
        self.point = point
        self.possible_connecting_points: List[Point] = possible_connecting_points
        self.connected_pipes: List = []
        self.connected_points: List[Point] = []

    def get_next_pipe(self, incoming_pipe):
        if self.is_dud or self.is_starting_pipe:
            return None
        index_of_incoming_pipe = self.connected_points.index(incoming_pipe.point)
        for index, pipe in enumerate(self.connected_pipes):
            if index != index_of_incoming_pipe:
                return pipe
        return None

    def add_connected_pipe(self, pipe):
        if pipe.point not in self.connected_points:
            self.connected_pipes.append(pipe)
            self.connected_points.append(pipe.point)

    @classmethod
    def create_pipe_from_string(cls, string: str, point: Point):
        neighbour_diffs = PIPE_STR_TO_VALID_NEIGHBOUR_DIFF[string]
        possible_connecting_points = [Point(point.x + diff.x, point.y + diff.y) for diff in neighbour_diffs]
        is_starting_point = string == "S"
        is_dud = string == "."
        return Pipe(string, point, possible_connecting_points, is_starting_point, is_dud)

    @classmethod
    def connect_pipes(cls, pipe_1, pipe_2):
        if pipe_1.point in pipe_2.possible_connecting_points and pipe_2.point in pipe_1.possible_connecting_points:
            if pipe_2.point not in pipe_1.connected_points:
                pipe_1.add_connected_pipe(pipe_2)
            if pipe_1.point not in pipe_2.connected_points:
                pipe_2.add_connected_pipe(pipe_1)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Pipe(content={self.content}, point={self.point}, connected_points={self.connected_points})"
