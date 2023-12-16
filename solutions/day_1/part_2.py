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


def part_2(lines: List[str]):
    pattern = re.compile(r"\d|" + "|".join([f"({key})" for key in WORDS_TO_NUM_MAP.keys()]))
    reverse_pattern = re.compile(r"\d|" + "|".join([f"({key[::-1]})" for key in WORDS_TO_NUM_MAP.keys()]))
    calibration_total = 0
    for line in lines:
        start = -1
        end = -1
        for match in pattern.finditer(line):
            start = match.group(0)
            break
        for match in reverse_pattern.finditer(line[::-1]):
            end = match.group(0)
            break
        start = WORDS_TO_NUM_MAP.get(start, start)
        end = WORDS_TO_NUM_MAP.get(end[::-1], end)
        calibration_value = int(f"{start}{end}")
        calibration_total += calibration_value
    return calibration_total
