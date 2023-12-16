import re
from typing import List, Union
from solutions.day_5.range_util import Range


def part_2(lines: List[str]):
    seed_ranges = []
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
            seed_range_pattern = re.compile("(?P<range_start>\d+)\s(?P<range_length>\d+)")
            for seed_range_match in seed_range_pattern.finditer(seed_match.group("seed_numbers")):
                start = int(seed_range_match.group("range_start"))
                length_of_range = int(seed_range_match.group("range_length"))
                seed_range = Range(start, start + length_of_range - 1, start, start + length_of_range - 1)
                insertion_index = find_index_of_first_smallest(seed_ranges, seed_range)
                seed_ranges.insert(insertion_index, seed_range)

        elif next_map_name_match:
            source_domain = next_map_name_match.group("source")
            target_domain = next_map_name_match.group("target")
            maps[source_domain] = {target_domain: []}

        elif mapping_match:
            destination_start = int(mapping_match.group("destination_start"))
            source_start = int(mapping_match.group("source_start"))
            range_length = int(mapping_match.group("range_length")) - 1
            a_range = Range(source_start, source_start+range_length, destination_start, destination_start+range_length)
            insertion_index = find_index_of_first_smallest(maps[source_domain][target_domain], a_range)
            maps[source_domain][target_domain].insert(insertion_index, a_range)

    final_ranges = []
    for seed_range in seed_ranges:
        source_domain = "seed"
        target_domain = list(maps[source_domain].keys())[0]
        current_ranges = [seed_range]
        while target_domain is not None:
            next_current_ranges = []
            for a_range in current_ranges:
                current_source_start = a_range.source_start
                current_source_end = a_range.source_end
                target_domain_ranges: List[Range] = maps[source_domain][target_domain]
                left_range_index = find_left_range_index(target_domain_ranges, a_range)
                right_range_index = find_right_range_index(target_domain_ranges, a_range)
                if ((left_range_index == -1 and right_range_index == -1) or
                        (left_range_index == len(target_domain_ranges) and right_range_index == len(target_domain_ranges))):
                    next_current_ranges.append(Range(current_source_start, current_source_end, current_source_start, current_source_end))
                    continue

                for range_index in range(left_range_index, right_range_index + 1):
                    if range_index == len(target_domain_ranges):
                        next_current_ranges.append(Range(current_source_start, a_range.source_end, current_source_start, a_range.source_end))
                        current_source_start = current_source_end + 1

                    else:
                        mapped_range = target_domain_ranges[range_index].map_from_source_range(
                            Range(current_source_start, current_source_end, current_source_start, current_source_end)
                        )
                        if mapped_range is None:
                            next_current_ranges.append(
                                Range(current_source_start, current_source_end, current_source_start,
                                      current_source_end)
                            )
                            current_source_start = current_source_end + 1
                        else:
                            if current_source_start < mapped_range.source_start:
                                next_current_ranges.append(
                                    Range(current_source_start, mapped_range.source_start-1, current_source_start, mapped_range.source_start-1)
                                )
                            next_current_ranges.append(
                                Range(mapped_range.destination_start, mapped_range.destination_end, mapped_range.destination_start, mapped_range.destination_end)
                            )
                            current_source_start = mapped_range.source_end + 1

                    if current_source_start > a_range.source_end:
                        break

            if target_domain in maps:
                source_domain = target_domain
                target_domain = list(maps[source_domain].keys())[0]
            else:
                target_domain = None
            current_ranges = merge_ranges(sorted(next_current_ranges))
        final_ranges.extend(current_ranges)
        final_ranges = sorted(final_ranges)

    return min([a_range.source_start for a_range in final_ranges])


def merge_ranges(ranges: List[Range]):
    if len(ranges) < 1:
        return []
    merged_ranges: List[Range] = []
    current_range = ranges[0]
    for a_range in ranges:
        if current_range.contains_value(a_range.source_start):
            current_range = Range(
                current_range.source_start, a_range.source_end,
                current_range.destination_start, a_range.destination_end
            )
        else:
            merged_ranges.append(current_range)
            current_range = a_range
    if len(merged_ranges) == 0 or merged_ranges[-1] != current_range:
        merged_ranges.append(current_range)
    return merged_ranges


def find_range_that_contains_value(ranges: List[Range], value) -> Union[Range, None]:
    for a_range in ranges:
        if a_range == value:
            return a_range
    return None


def find_left_range_index(ranges: List[Range], search_range: Range) -> int:
    for index, a_range in enumerate(ranges):
        if a_range.contains_value(search_range.source_start):
            return index
        if search_range.source_start < a_range.source_start:
            return index - 1
    return len(ranges)


def find_right_range_index(ranges: List[Range], search_range: Range) -> int:
    for index, a_range in enumerate(ranges):
        if a_range.contains_value(search_range.source_end) or search_range.source_end < a_range.source_start:
            return index
    return len(ranges)


def find_index_of_first_largest_range(ranges: List[Range], value: int):
    first_smallest_index = 0
    for index, current_range in enumerate(ranges):
        first_smallest_index = index
        if current_range.source_start > value:
            break
    else:
        return first_smallest_index + 1
    return first_smallest_index


def find_index_of_first_smallest(ranges: List[Range], a_range: Range):
    first_smallest_index = 0
    for index, current_range in enumerate(ranges):
        first_smallest_index = index
        if a_range.source_start < current_range.source_start:
            break
    else:
        return first_smallest_index + 1
    return first_smallest_index
