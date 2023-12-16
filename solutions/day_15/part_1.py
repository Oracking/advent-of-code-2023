from typing import List


def part_1(lines: List[str]):
    initialization_sequence = lines[0].split(",")
    sum_score = 0
    for sequence in initialization_sequence:
        sequence_score = 0
        for char in sequence:
            sequence_score = ((sequence_score + ord(char)) * 17) % 256
        sum_score += sequence_score
    return sum_score
