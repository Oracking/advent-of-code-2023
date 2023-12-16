import re
from typing import List

WORDS_TO_NUM_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def part_1(lines: List[str]):
    pattern = re.compile(r"\d")
    calibration_total = 0
    for line in lines:
        start = end = None
        for index, match in enumerate(pattern.finditer(line)):
            if index == 0:
                start = match.group(0)
            end = match.group(0)
        calibration_value = int(f"{start}{end}")
        calibration_total += calibration_value
    return calibration_total

