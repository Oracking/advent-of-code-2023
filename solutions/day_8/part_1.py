import re
from typing import List

direction_to_index = {
    "L": 0,
    "R": 1
}


def part_1(lines: List[str]):
    source_node_to_destination_nodes = {}
    direction_stream = list(lines[0])
    node_pattern = re.compile(r"(?P<current_node>\w+)\s=\s\((?P<left_node>\w+),\s(?P<right_node>\w+)\)")
    for line in lines[2:]:
        match = node_pattern.match(line)
        source_node_to_destination_nodes[match.group("current_node")] = [match.group("left_node"), match.group("right_node")]

    current_node = "AAA"
    destination_node = "ZZZ"
    direction_stream_index = 0
    movement_count = 0
    while current_node != destination_node:
        direction_index = direction_to_index[direction_stream[direction_stream_index]]
        current_node = source_node_to_destination_nodes[current_node][direction_index]
        direction_stream_index = (direction_stream_index + 1) % len(direction_stream)
        movement_count += 1
    return movement_count
