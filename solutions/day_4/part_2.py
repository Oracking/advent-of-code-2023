import re
from typing import List


def part_2(lines: List[str]):
    line_pattern = re.compile(
        r"Card\s*(?P<card_number>\d+):(?P<winning_numbers>[^|]*)\|(?P<owned_numbers>.*)"
    )
    numbers_pattern = re.compile(r"\d+")

    card_counts = {}
    for i in range(len(lines)):
        card_counts[i+1] = 1

    for line in lines:
        line_match = line_pattern.match(line)
        card_number = int(line_match.group("card_number"))
        winning_numbers = set((int(str_number) for str_number in numbers_pattern.findall(line_match.group("winning_numbers"))))
        owned_numbers = set((int(str_number) for str_number in numbers_pattern.findall(line_match.group("owned_numbers"))))
        card_score = len(winning_numbers.intersection(owned_numbers))
        num_new_copies = card_counts[card_number]
        for i in range(card_score):
            card_counts[card_number + i + 1] += num_new_copies

    return sum(card_counts.values())

