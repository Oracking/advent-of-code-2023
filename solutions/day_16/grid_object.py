from typing import Dict, Tuple, List
from utils.grid import Point


class GridObject:
    NEXT_BEAM_DIRECTIONS: Dict[str, Dict[Point, Tuple[Point]]] = {
        "/": {
            Point(1, 0): (Point(0, -1),),
            Point(-1, 0): (Point(0, 1),),
            Point(0, 1): (Point(-1, 0),),
            Point(0, -1): (Point(1, 0),),
        },
        "\\": {
            Point(1, 0): (Point(0, 1),),
            Point(-1, 0): (Point(0, -1),),
            Point(0, 1): (Point(1, 0),),
            Point(0, -1): (Point(-1, 0),),
        },
        "|": {
            Point(1, 0): (Point(0, -1), Point(0, 1)),
            Point(-1, 0): (Point(0, -1), Point(0, 1)),
            Point(0, 1): (Point(0, 1),),
            Point(0, -1): (Point(0, -1),),
        },
        "-": {
            Point(1, 0): (Point(1, 0),),
            Point(-1, 0): (Point(-1, 0),),
            Point(0, 1): (Point(-1, 0), Point(1, 0)),
            Point(0, -1): (Point(-1, 0), Point(1, 0)),
        },
        ".": {
            Point(1, 0): (Point(1, 0),),
            Point(-1, 0): (Point(-1, 0),),
            Point(0, 1): (Point(0, 1),),
            Point(0, -1): (Point(0, -1),),
        }
    }

    def __init__(self, object_type: str, coordinate: Point):
        self.object_type = object_type
        self.coordinate: Point = coordinate
        self.output_direction_cache: List[Point] = []
        self.is_active = False

    def get_next_beam_positions(self, previous_beam_position: Point) -> List[Point]:
        self.is_active = True
        beam_direction = (self.coordinate.x - previous_beam_position.x, self.coordinate.y - previous_beam_position.y)
        possible_directions: Tuple[Point] = self.NEXT_BEAM_DIRECTIONS[self.object_type][beam_direction]
        new_directions = [direction for direction in possible_directions if
                          direction not in self.output_direction_cache]
        next_beam_positions = []
        for direction in new_directions:
            next_point = Point(self.coordinate.x + direction.x, self.coordinate.y + direction.y)
            next_beam_positions.append(next_point)
            self.output_direction_cache.append(direction)
        return next_beam_positions

    def reset(self):
        self.is_active = False
        self.output_direction_cache = []

    def __repr__(self):
        return self.object_type
