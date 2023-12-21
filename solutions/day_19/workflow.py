import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class InputRange:
    lower_bound: int = 0
    upper_bound: int = 4001

    def copy(self):
        return InputRange(self.lower_bound, self.upper_bound)

    def num_values_in_range(self) -> int:
        return self.upper_bound - self.lower_bound - 1


@dataclass
class WorkflowInputRange:
    x: InputRange = InputRange()
    m: InputRange = InputRange()
    a: InputRange = InputRange()
    s: InputRange = InputRange()

    def is_valid(self):
        return ((self.x.num_values_in_range() > 0) and
                (self.m.num_values_in_range() > 0) and
                (self.a.num_values_in_range() > 0) and
                (self.s.num_values_in_range() > 0))

    def copy(self):
        return WorkflowInputRange(
            self.x.copy(), self.m.copy(), self.a.copy(), self.s.copy()
        )

    def num_values_in_range(self):
        return (
                self.x.num_values_in_range() *
                self.m.num_values_in_range() *
                self.a.num_values_in_range() *
                self.s.num_values_in_range()
        )


@dataclass
class WorkflowInput:
    x: int
    m: int
    a: int
    s: int


@dataclass
class WorkflowInputResult:
    workflow_input: WorkflowInput
    action: str


@dataclass
class WorkflowInputRangeResult:
    passing_range: WorkflowInputRange
    failing_range: WorkflowInputRange
    action: str


class WorkflowOperation:

    OPERATION_PATTERN = re.compile("((?P<upper_domain>\w)<(?P<upper>\d+))|((?P<lower_domain>\w)>(?P<lower>\d+))")

    def __init__(self, operation: str, action: str):
        self.operation = operation
        self.action = action
        self.success_ranges: Dict[str, InputRange] = {
            "x": InputRange(),
            "m": InputRange(),
            "a": InputRange(),
            "s": InputRange(),
        }
        self.failure_ranges: Dict[str, InputRange] = {
            "x": InputRange(),
            "m": InputRange(),
            "a": InputRange(),
            "s": InputRange(),
        }
        self.set_input_ranges()

    def set_input_ranges(self):
        if self.operation is not None:
            operation_match = self.OPERATION_PATTERN.match(self.operation)
            upper_domain = operation_match.group("upper_domain")
            str_upper = operation_match.group("upper")
            lower_domain = operation_match.group("lower_domain")
            str_lower = operation_match.group("lower")
            if upper_domain:
                self.failure_ranges[upper_domain].lower_bound = max(
                    int(str_upper) - 1, self.failure_ranges[upper_domain].lower_bound
                )
                self.success_ranges[upper_domain].upper_bound = min(
                    int(str_upper), self.success_ranges[upper_domain].upper_bound
                )
            if lower_domain:
                self.failure_ranges[lower_domain].upper_bound = min(
                    int(str_lower) + 1, self.failure_ranges[lower_domain].upper_bound
                )
                self.success_ranges[lower_domain].lower_bound = max(
                    int(str_lower), self.success_ranges[lower_domain].lower_bound
                )

    def process(self, workflow_input: WorkflowInput) -> WorkflowInputResult:
        if self.operation:
            templated_operation = self.operation
            templated_operation = templated_operation.replace("x", "workflow_input.x")
            templated_operation = templated_operation.replace("m", "workflow_input.m")
            templated_operation = templated_operation.replace("a", "workflow_input.a")
            templated_operation = templated_operation.replace("s", "workflow_input.s")
            operation_result = eval(templated_operation)
            if operation_result:
                return WorkflowInputResult(workflow_input, self.action)
            return WorkflowInputResult(workflow_input, None)
        return WorkflowInputResult(workflow_input, self.action)

    def process_input_range(self, current_workflow_input_range: WorkflowInputRange) -> WorkflowInputRangeResult:
        passing_range_to_return = current_workflow_input_range.copy()
        failure_range_to_return = current_workflow_input_range.copy()
        for domain, success_range in self.success_ranges.items():
            current_range = passing_range_to_return.__getattribute__(domain)
            current_range.lower_bound = max(success_range.lower_bound, current_range.lower_bound)
            current_range.upper_bound = min(success_range.upper_bound, current_range.upper_bound)

            current_range = failure_range_to_return.__getattribute__(domain)
            current_range.lower_bound = max(self.failure_ranges[domain].lower_bound, current_range.lower_bound)
            current_range.upper_bound = min(self.failure_ranges[domain].upper_bound, current_range.upper_bound)
        return WorkflowInputRangeResult(passing_range_to_return, failure_range_to_return, self.action)


class Workflow:
    def __init__(self, name, operations: List[WorkflowOperation]):
        self.name: str = name
        self.operations: List[WorkflowOperation] = operations

    def process_input(self, workflow_input: WorkflowInput) -> str:
        for operation in self.operations:
            operation_result = operation.process(workflow_input)
            if operation_result.action:
                return operation.action

    def process_input_range(self, workflow_input_range: WorkflowInputRange) -> List[WorkflowInputRangeResult]:
        results: List[WorkflowInputRangeResult] = []
        current_input_range = workflow_input_range
        for operation in self.operations:
            range_result = operation.process_input_range(current_input_range)
            current_input_range = range_result.failing_range
            if range_result.passing_range.is_valid() and not range_result.action == "R":
                results.append(WorkflowInputRangeResult(range_result.passing_range, None, range_result.action))
            if not current_input_range.is_valid():
                break
        return results

    @classmethod
    def create_workflow_from_string(cls, input_str: str):
        full_line_pattern = re.compile(r"(?P<workflow_name>\w+)\{(?P<workflow_instructions>[^}]+)\}")
        instructions_pattern = re.compile(
            r"((?P<eval_body>[^:]+):(?P<action_1>\w+),?)|(?P<action_2>\w+)")
        full_line_match = full_line_pattern.match(input_str)
        workflow_name = full_line_match.group("workflow_name")

        workflow_operations: List[WorkflowOperation] = []
        for instructions_match in instructions_pattern.finditer(full_line_match.group("workflow_instructions")):
            operation = instructions_match.group("eval_body")
            action = instructions_match.group("action_1") or instructions_match.group("action_2")
            workflow_operations.append(WorkflowOperation(operation, action))

        return Workflow(workflow_name, workflow_operations)