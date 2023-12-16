import re
from typing import List


def part_1(lines: List[str]):
    colors_max = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    line_pattern = re.compile(r"Game\s(?P<game_number>\d+):(?P<game_results>.*)")
    single_move_results = re.compile(r"\d[^;]+")
    color_number_pattern = re.compile(r"(?P<color_number>\d+)\s(?P<color_name>[^,]+)")

    impossible_games = []
    possible_games = []

    for line in lines:
        line_match = line_pattern.match(line)
        game_number = line_match.group("game_number")
        exit_game = False
        for single_move_result_match in single_move_results.finditer(line_match.group("game_results")):
            for color_count_match in color_number_pattern.finditer(single_move_result_match.group(0)):
                if int(color_count_match.group("color_number")) > colors_max[color_count_match.group("color_name")]:
                    impossible_games.append(int(game_number))
                    exit_game = True
                    break
            if exit_game:
                break
        else:
            possible_games.append(int(game_number))
    return sum(possible_games)
