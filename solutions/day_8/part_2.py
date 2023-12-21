from math import gcd
import re
from typing import List
from utils.custom_math import lcm

direction_to_index = {
    "L": 0,
    "R": 1
}


def part_2(lines: List[str]):
    source_node_to_destination_nodes = {}
    direction_stream = list(lines[0])
    node_pattern = re.compile(r"(?P<current_node>\w+)\s=\s\((?P<left_node>\w+),\s(?P<right_node>\w+)\)")
    for line in lines[2:]:
        match = node_pattern.match(line)
        source_node_to_destination_nodes[match.group("current_node")] = [match.group("left_node"), match.group("right_node")]

    current_nodes = set(node for node in source_node_to_destination_nodes.keys() if node.endswith("A"))
    z_point_loops = []
    for node in current_nodes:
        z_point_loops.append(find_z_points_loop(source_node_to_destination_nodes, direction_stream, node))

    # The code below is an optimization.
    # WB: And I can perform the below optimization because I've had a look at the data and noticed that
    # each loop contains exactly one point that ends in Z. And the distance from the start to that z-point
    # is the same as the distance from the z-point, to the end and back to itself. Effectively, the z-point
    # loops are looking like this:
    # [
    #   [(1, 14999), (0, 14999)], [(1, 12169), (0, 12169)], [(1, 13301), (0, 13301)],
    #   [(1, 16697), (0, 16697)], [(1, 17263), (0, 17263)], [(1, 18961), (0, 18961)]
    # ]
    loop_lengths = [loop[0][1] for loop in z_point_loops]
    return lcm(*tuple(loop_lengths))


def find_z_points_loop(source_node_to_destination_nodes, direction_stream, node):
    current_node = node
    direction_stream_index = 0
    movement_count = 0
    traversed_nodes = set()
    traversed_nodes_list = list()
    while True:
        if (current_node, direction_stream_index) not in traversed_nodes:
            traversed_nodes.add((current_node, direction_stream_index))
            traversed_nodes_list.append((current_node, direction_stream_index))
        direction_index = direction_to_index[direction_stream[direction_stream_index]]
        current_node = source_node_to_destination_nodes[current_node][direction_index]
        direction_stream_index = (direction_stream_index + 1) % len(direction_stream)
        movement_count += 1
        if (current_node, direction_stream_index) in traversed_nodes:
            break

    return convert_traversed_nodes_to_z_points(traversed_nodes_list, traversed_nodes_list.index((current_node, direction_stream_index)))


def convert_traversed_nodes_to_z_points(traversed_nodes_list, loop_back_index):
    movement_count = 0
    index = 1
    z_points = []
    for node, _ in traversed_nodes_list[1:]:
        movement_count += 1
        if node.endswith("Z"):
            z_points.append((1, movement_count))
            index += 1
            movement_count = 0

    z_points.append((0, movement_count+1 + z_points[0][1] - loop_back_index))
    return z_points



