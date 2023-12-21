import functools
import re
from typing import List, Union, Tuple


def part_2(lines: List[str]):
    line_pattern = re.compile(r"(?P<input_pattern>[#.?]+)\s(?P<target_pattern>[\d,]+)")
    total_num_ways = 0
    fixed_insertions = generate_fixed_insertions()
    for index, line in enumerate(lines):
        print(f"Test case: {index+1} / {len(lines)}")
        line_match = line_pattern.match(line)
        input_pattern = line_match.group("input_pattern")
        target_pattern = [int(value) for value in line_match.group("target_pattern").split(",")]
        num_ways_for_test_case = expand_and_solve(input_pattern, target_pattern, fixed_insertions)
        print("Number of ways for test case: ", num_ways_for_test_case)
        total_num_ways += num_ways_for_test_case
    return total_num_ways


def expand_and_solve(input_pattern, target_pattern: List[int], fixed_insertions: List[List[str]]) -> int:
    total_num_ways = 0
    duplicated_target_pattern = [value for sub_list in [target_pattern] * 5 for value in sub_list]
    for index, fixed_insertion in enumerate(fixed_insertions):
        print(f"    Child progress: {index+1} / {len(fixed_insertions)}")
        duplicated_input = ""
        for insertion_value in fixed_insertion:
            duplicated_input += (input_pattern + insertion_value)
        instance_num_ways = recursive_match(duplicated_input, tuple(duplicated_target_pattern))
        total_num_ways += instance_num_ways
    return total_num_ways


def generate_fixed_insertions():
    insertions = []
    for i in ["#", "."]:
        for j in ["#", "."]:
            for k in ["#", "."]:
                for l in ["#", "."]:
                        insertions.append([i, j, k, l, ""])
    return insertions


@functools.lru_cache()
def recursive_match(input_pattern: str, target_pattern: Tuple[int]) -> int:
    if len(target_pattern) == 0:
        if "#" in input_pattern:
            return 0
        return 1
    if len(input_pattern) == 0:
        return 0

    num_solutions = 0
    from_index = 0
    target_length = target_pattern[0]
    hard_stop = input_pattern.find("#")

    match_index = find_next_match(input_pattern, from_index, target_length)
    while match_index is not None:
        if we_are_matching_after_hard_stop(hard_stop, match_index):
            break
        num_sub_solutions = recursive_match(input_pattern[match_index + target_length + 1:], target_pattern[1:])
        if num_sub_solutions > 0:
            num_solutions += num_sub_solutions
        from_index = find_next_instance(input_pattern, match_index, ".") + 1
        match_index = find_next_match(input_pattern, from_index, target_length)
    return num_solutions


def we_are_matching_after_hard_stop(hard_stop, match_index):
    if hard_stop > -1:
        if match_index is not None and match_index > hard_stop:
            return True
    return False


def find_next_match(input_pattern: str, from_index: int,  target_length: int) -> Union[int, None]:
    for start_index in range(from_index, len(input_pattern)):
        sub_pattern_end_index = start_index
        while sub_pattern_end_index - start_index < target_length and sub_pattern_end_index < len(input_pattern):
            next_char = input_pattern[sub_pattern_end_index]
            if char_can_be(next_char, "#"):
                sub_pattern_end_index += 1
            else:
                break
        if sub_pattern_end_index - start_index == target_length:
            if sub_pattern_end_index == len(input_pattern) or char_can_be(input_pattern[sub_pattern_end_index], "."):
                return start_index
    return None


def find_next_instance(input_string, from_index, character):
    for i in range(from_index, len(input_string)):
        if char_can_be(input_string[i], character):
            return i
    return len(input_string)


def char_can_be(character, target_character):
    return character == target_character or character == "?"
