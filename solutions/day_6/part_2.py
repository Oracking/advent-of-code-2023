import math
from typing import List


def quadratic_solutions(t, d):
    sol_1 = (-t + (t**2 - 4 * -1 * -d)**0.5) / (2*(-1))
    sol_2 = (-t - (t**2 - 4 * -1 * -d)**0.5) / (2*(-1))
    return (sol_1, sol_2)


def part_2(lines: List[str]):
    times_str = lines[0].strip("Time:")
    distances_str = lines[1].strip("Distance:")

    time = int(times_str.replace(" ", ""))
    distance = int(distances_str.replace(" ", ""))

    lower_bound, upper_bound = quadratic_solutions(time, distance)
    minimum_seconds = max(math.ceil(lower_bound), math.floor(lower_bound) + 1)
    maximum_seconds = min(math.floor(upper_bound), math.ceil(upper_bound) - 1)
    total_valid_values = (maximum_seconds - minimum_seconds) + 1

    return total_valid_values
