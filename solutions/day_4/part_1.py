import re
from typing import List


def part_1(lines: List[str]):
    line_pattern = re.compile(
        r"Card\s*(?P<card_number>\d+):(?P<winning_numbers>[^|]*)\|(?P<owned_numbers>.*)"
    )
    numbers_pattern = re.compile(r"\d+")

    total_points = 0

    for line in lines:
        line_match = line_pattern.match(line)
        winning_numbers = set((int(str_number) for str_number in numbers_pattern.findall(line_match.group("winning_numbers"))))
        owned_numbers = set((int(str_number) for str_number in numbers_pattern.findall(line_match.group("owned_numbers"))))
        if len(winning_numbers.intersection(owned_numbers)) > 0:
            card_points = 2 ** (len(winning_numbers.intersection(owned_numbers)) - 1)
            total_points += card_points

    return total_points