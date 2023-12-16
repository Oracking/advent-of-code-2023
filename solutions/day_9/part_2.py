from typing import List


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def lagrange_interpolate(f: list, xi: int, n: int) -> float:
    result = 0.0
    for i in range(n):
        term = f[i].y
        for j in range(n):
            if j != i:
                term = term * (xi - f[j].x) / (f[i].x - f[j].x)
        result += term
    return result


def part_2(lines: List[str]):
    list_of_y_values = [line.split(" ") for line in lines]
    interpolation_results = []
    for y_values in list_of_y_values:
        points = [Data(i, int(x)) for i, x in enumerate(y_values)]
        interpolation_results.append(round(lagrange_interpolate(points, -1, len(points))))
    return sum(interpolation_results)