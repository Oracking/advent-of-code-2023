import re
from typing import List


def part_2(lines: List[str]):
    line_pattern = re.compile(r"Game\s(?P<game_number>\d+):(?P<game_results>.*)")
    single_move_results = re.compile(r"\d[^;]+")
    color_number_pattern = re.compile(r"(?P<color_number>\d+)\s(?P<color_name>[^,]+)")

    total_power_score = 0

    for line in lines:
        minimum_colors = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        line_match = line_pattern.match(line)
        for single_move_result_match in single_move_results.finditer(line_match.group("game_results")):
            for color_count_match in color_number_pattern.finditer(single_move_result_match.group(0)):
                color_name = color_count_match.group("color_name")
                color_number = color_count_match.group("color_number")
                minimum_colors[color_name] = max([minimum_colors[color_name], int(color_number)])
        total_power_score += minimum_colors["red"] * minimum_colors["blue"] * minimum_colors["green"]
    return total_power_score
