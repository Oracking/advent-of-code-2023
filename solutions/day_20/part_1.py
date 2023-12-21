import re
from typing import List
from solutions.day_20.modules import FlipFlop, Conjunction, BroadCaster, DummyModule, Signal


def part_1(lines: List[str]):
    module_name_to_module = create_module_name_to_module_map(lines)
    signal_counts = {0: 0, 1: 0}
    for _ in range(1000):
        iteration_signal_counts = simulate_button_press(module_name_to_module)
        signal_counts[0] += iteration_signal_counts[0]
        signal_counts[1] += iteration_signal_counts[1]
    return signal_counts[0] * signal_counts[1]


def simulate_button_press(module_name_to_module_map):
    current_signals: List[Signal] = [Signal(DummyModule("button"), 0, [module_name_to_module_map["broadcaster"]])]
    signal_counts = {0: 0, 1: 0}
    while len(current_signals) > 0:
        next_signals: List[Signal] = []
        for signal in current_signals:
            signal_counts[signal.bit_signal] += len(signal.destination_modules)
            for destination_module in signal.destination_modules:
                new_signal: Signal = destination_module.process_input(signal)
                if new_signal.bit_signal is not None:
                    next_signals.append(new_signal)
        current_signals = next_signals
    return signal_counts


def create_module_name_to_module_map(lines: List[str]):
    module_name_to_module = {}
    line_pattern = re.compile(
        r"(?P<source_module>(?P<broadcaster>broadcaster)|(?P<flip_flop>%\w+)|(?P<conjunction>&\w+))\s->\s(?P<connected_modules>.*)")
    for line in lines:
        line_match = line_pattern.match(line)
        if line_match.group("broadcaster"):
            module = BroadCaster()
        elif line_match.group("flip_flop"):
            module = FlipFlop(line_match.group("flip_flop").strip("%"))
        else:
            module = Conjunction(line_match.group("conjunction").strip("&"))
        module_name_to_module[module.name] = module

    for line in lines:
        line_match = line_pattern.match(line)
        source_module_name = line_match.group("source_module").strip("%").strip("&")
        source_module = module_name_to_module[source_module_name]
        connected_module_names = [name.strip(" ") for name in line_match.group("connected_modules").split(",")]

        for output_module_name in connected_module_names:
            if output_module_name not in module_name_to_module:
                dummy_module = DummyModule(output_module_name)
                source_module.output_modules.append(dummy_module)
                dummy_module.add_input_module(source_module.name)
                module_name_to_module[output_module_name] = dummy_module
            else:
                output_module = module_name_to_module[output_module_name]
                output_module.add_input_module(source_module.name)
                source_module.output_modules.append(output_module)
    return module_name_to_module
