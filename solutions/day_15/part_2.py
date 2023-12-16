import re
from collections import namedtuple
from typing import Dict, List

Lens = namedtuple("Lens", ("label", "focal_length"))
IndexedLens = namedtuple("IndexedLens", ("label", "focal_length", "index"))


class Box:
    def __init__(self, number: int):
        self.number = number
        self.label_to_lens: Dict[str, IndexedLens] = {}
        self.next_insertion_count = 0

    def add_lens(self, lens: Lens):
        existing_lens = self.label_to_lens.get(lens.label, None)
        if existing_lens is not None:
            replacement_lens = IndexedLens(lens.label, lens.focal_length, existing_lens.index)
            self.label_to_lens[lens.label] = replacement_lens
            return
        self.label_to_lens[lens.label] = IndexedLens(lens.label, lens.focal_length, self.next_insertion_count)
        self.next_insertion_count += 1

    def remove_lens(self, lens: Lens):
        if lens.label in self.label_to_lens:
            del self.label_to_lens[lens.label]

    def calc_power(self):
        total_power = 0
        for true_index, lens in enumerate(sorted(self.label_to_lens.values(), key=lambda lens: lens.index)):
            total_power += (self.number + 1) * (true_index + 1) * lens.focal_length
        return total_power


def part_2(lines: List[str]):
    pattern = re.compile(r"(?P<insertion>(?P<insertion_label>[^=]+)=(?P<focal_length>\d+))|(?P<removal>(?P<removal_label>[^-]+)-)")
    initialization_sequence = lines[0].split(",")
    boxes: List[Box] = create_boxes()
    for sequence in initialization_sequence:
        match = pattern.match(sequence)
        if match.group("insertion"):
            label: str = match.group("insertion_label")
            focal_length = int(match.group("focal_length"))
            box_number = convert_sequence_to_ascii_value(label)
            boxes[box_number].add_lens(Lens(label, focal_length))
        else:
            label: str = match.group("removal_label")
            box_number = convert_sequence_to_ascii_value(label)
            boxes[box_number].remove_lens(Lens(label, 0))
    return sum([box.calc_power() for box in boxes])


def create_boxes() -> List[Box]:
    boxes: List[Box] = []
    for i in range(0, 256):
        boxes.append(Box(i))
    return boxes


def convert_sequence_to_ascii_value(sequence: str) -> int:
    sequence_score = 0
    for char in sequence:
        sequence_score = ((sequence_score + ord(char)) * 17) % 256
    return sequence_score