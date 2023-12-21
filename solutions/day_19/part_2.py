from typing import List, Dict
from solutions.day_19.workflow import Workflow, WorkflowInputRange, WorkflowInputRangeResult


def part_2(lines: List[str]):
    workflow_name_to_workflow_map: Dict[str, Workflow] = {}
    for index, line in enumerate(lines):
        if len(line) == 0:
            break
        workflow = Workflow.create_workflow_from_string(line)
        workflow_name_to_workflow_map[workflow.name] = workflow
    valid_ranges: List[WorkflowInputRange] = get_valid_ranges(workflow_name_to_workflow_map)

    # WB: The line that follows this comment produces the correct value because the ranges do
    # not overlap (I checked that they don't :)). If they overlapped we would have had to use the
    # inclusion-exclusion principle, https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle, to
    # calculate the number of distinct values in the ranges
    return sum([a_range.num_values_in_range() for a_range in valid_ranges])


def get_valid_ranges(workflow_name_to_workflow_map: Dict[str, Workflow]):
    accepted_ranges: List[WorkflowInputRange] = []
    current_range_results: List[WorkflowInputRangeResult] = [WorkflowInputRangeResult(WorkflowInputRange(), None, "in")]
    while len(current_range_results) > 0:
        next_range_results: List[WorkflowInputRangeResult] = []
        for input_range_result in current_range_results:
            if input_range_result.action == "A":
                accepted_ranges.append(input_range_result.passing_range)
            else:
                workflow = workflow_name_to_workflow_map[input_range_result.action]
                next_range_results.extend(
                    workflow.process_input_range(input_range_result.passing_range)
                )
        current_range_results = next_range_results
    return accepted_ranges
