import re
import math
from typing import List


def quadratic_solutions(t, d):
    sol_1 = (-t + (t**2 - 4 * -1 * -d)**0.5) / (2*(-1))
    sol_2 = (-t - (t**2 - 4 * -1 * -d)**0.5) / (2*(-1))
    return (sol_1, sol_2)


def part_1(lines: List[str]):
    times_str = lines[0].strip("Time:")
    distances_str = lines[1].strip("Distance:")
    numbers_pattern = re.compile("\d+")

    times = [int(number_match) for number_match in numbers_pattern.findall(times_str)]
    distances = [int(number_match) for number_match in numbers_pattern.findall(distances_str)]

    final_score = 1
    for time, distance in zip(times, distances):
        lower_bound, upper_bound = quadratic_solutions(time, distance)
        minimum_seconds = max(math.ceil(lower_bound), math.floor(lower_bound) + 1)
        maximum_seconds = min(math.floor(upper_bound), math.ceil(upper_bound) - 1)
        total_valid_values = (maximum_seconds - minimum_seconds) + 1
        final_score *= total_valid_values
    return final_score
