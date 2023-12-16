import re
from typing import List, Union
from solutions.day_5.range_util import Range


def part_1(lines: List[str]):
    seeds = []
    maps = {}

    seed_pattern = re.compile(r"seeds:(?P<seed_numbers>.*)")
    next_map_name_pattern = re.compile(r"(?P<source>\w+)-to-(?P<target>\w+)\smap")
    mapping_pattern = re.compile(r"(?P<destination_start>\d+)\s(?P<source_start>\d+)\s(?P<range_length>\d+)")

    source_domain = None
    target_domain = None
    for line in lines:
        seed_match = seed_pattern.match(line)
        next_map_name_match = next_map_name_pattern.match(line)
        mapping_match = mapping_pattern.match(line)
        if seed_match:
            numbers_pattern = re.compile("\d+")
            for seed_number in numbers_pattern.finditer(seed_match.group("seed_numbers")):
                seeds.append(int(seed_number.group(0)))

        elif next_map_name_match:
            source_domain = next_map_name_match.group("source")
            target_domain = next_map_name_match.group("target")
            maps[source_domain] = {target_domain: []}

        elif mapping_match:
            destination_start = int(mapping_match.group("destination_start"))
            source_start = int(mapping_match.group("source_start"))
            range_length = int(mapping_match.group("range_length")) - 1
            range = Range(source_start, source_start+range_length, destination_start, destination_start+range_length)
            insertion_index = find_index_of_first_smallest(maps[source_domain][target_domain], range)
            maps[source_domain][target_domain].insert(insertion_index, range)

    seed_to_final_value = {}
    for seed in seeds:
        source_domain = "seed"
        current_value = seed
        target_domain = list(maps[source_domain].keys())[0]
        while target_domain is not None:
            if source_domain in maps:
                target_domain = list(maps[source_domain].keys())[0]
                range_match = find_range_that_contains_value(maps[source_domain][target_domain], current_value)
                if range_match is not None:
                    current_value = range_match.map_from_source(current_value)
                source_domain = target_domain
            else:
                target_domain = None
        seed_to_final_value[seed] = current_value

    return min(seed_to_final_value.values())


def find_range_that_contains_value(ranges: List[Range], value) -> Union[Range, None]:
    for a_range in ranges:
        if a_range == value:
            return a_range
    return None


def find_index_of_first_smallest(ranges: List[Range], a_range: Range):
    first_smallest_index = 0
    for index, current_range in enumerate(ranges):
        first_smallest_index = index
        if a_range.source_start < current_range.source_start:
            break
    else:
        return first_smallest_index + 1
    return first_smallest_index
