from typing import List, Dict
from solutions.day_19.workflow import Workflow, WorkflowInput


def part_1(lines: List[str]):
    workflow_name_to_workflow_map: Dict[str, Workflow] = {}
    workflow_inputs_start = 0
    for index, line in enumerate(lines):
        if len(line) == 0:
            workflow_inputs_start = index + 1
            break
        workflow = Workflow.create_workflow_from_string(line)
        workflow_name_to_workflow_map[workflow.name] = workflow

    workflow_inputs: List[WorkflowInput] = []
    for index in range(workflow_inputs_start, len(lines)):
        templated_line = lines[index].replace("{", "WorkflowInput(")
        templated_line = templated_line.replace("}", ")")
        workflow_inputs.append(eval(templated_line))

    final_score = 0
    for workflow_input in workflow_inputs:
        if input_is_accepted(workflow_input, workflow_name_to_workflow_map):
            final_score += workflow_input.x + workflow_input.m + workflow_input.a + workflow_input.s
    return final_score


def input_is_accepted(workflow_input: WorkflowInput, workflow_name_to_workflow_map: Dict[str, Workflow]):
    current_workflow_name = "in"
    while True:
        next_action = workflow_name_to_workflow_map.get(current_workflow_name).process_input(workflow_input)
        if next_action == "A":
            return True
        elif next_action == "R":
            return False
        current_workflow_name = next_action
