from typing import List, Dict
from solutions.day_20.modules import DummyModule, Signal, Conjunction
from solutions.day_20.part_1 import create_module_name_to_module_map
from utils.custom_math import lcm


def part_2(lines: List[str]):
    module_name_to_module_map = create_module_name_to_module_map(lines)
    if "rx" not in module_name_to_module_map:
        return 1

    # WB: With regards to the next line, I know there is only one input module because I checked
    # In fact, all the lines that follow make multiple assumptions (which I have validated against my input)
    # I'm not proud of this but it was required :(
    final_conjunction_name: Conjunction = module_name_to_module_map["rx"].input_modules[0]
    names_of_inputs_to_final_conjunction = module_name_to_module_map[final_conjunction_name].input_modules
    module_name_to_button_press_where_module_sent_a_high: Dict[str, List[int]] = {}
    for name in names_of_inputs_to_final_conjunction:
        module_name_to_button_press_where_module_sent_a_high[name] = []

    # WB: For the below loop I arrived at 10000 iterations through experimentation. It's the minimum number of
    # iterations after which we see the inputs to the final conjunction sending a high signal
    for iteration_number in range(10000):
        modules_that_sent_a_high = simulate_button_press(
            module_name_to_module_map,
            final_conjunction_name,
            names_of_inputs_to_final_conjunction
        )
        for name in names_of_inputs_to_final_conjunction:
            if name in modules_that_sent_a_high:
                module_name_to_button_press_where_module_sent_a_high[name].append(iteration_number+1)

        we_have_minimum_number_of_iterations_across_all_inputs = True
        for iteration_numbers in module_name_to_button_press_where_module_sent_a_high.values():
            if len(iteration_numbers) < 2:
                we_have_minimum_number_of_iterations_across_all_inputs = False

        if we_have_minimum_number_of_iterations_across_all_inputs:
            break
    return find_min_number_of_button_presses_for_all_modules_to_send_a_high(
        module_name_to_button_press_where_module_sent_a_high
    )


def find_min_number_of_button_presses_for_all_modules_to_send_a_high(
        module_name_to_button_press_where_module_sent_a_high
):
    # WB: All the nooses need to have started at the same index in their loop for below to work. I checked
    # and this is true for the input
    loop_lengths = []
    line_sizes = []
    for noose in module_name_to_button_press_where_module_sent_a_high.values():
        loop_lengths.append(noose[1] - noose[0])
        line_sizes.append(noose[0])

    # WB: We know the loop offsets are shared because we checked
    shared_loop_offset = loop_lengths[0] - line_sizes[0]
    return shared_loop_offset + lcm(*tuple(loop_lengths))

def simulate_button_press(
        module_name_to_module_map,
        final_conjunction_name,
        name_of_final_conjunction_input_modules
):
    current_signals: List[Signal] = [Signal(DummyModule("button"), 0, [module_name_to_module_map["broadcaster"]])]
    name_of_final_conjunction_input_modules_that_sent_a_high_signal = set()
    while len(current_signals) > 0:
        next_signals: List[Signal] = []
        for signal in current_signals:
            for destination_module in signal.destination_modules:
                for module_name in name_of_final_conjunction_input_modules:
                    is_a_high_signal_from_module_to_final_conjunction = (
                            signal.bit_signal == 1 and
                            signal.source_module.name == module_name and
                            destination_module.name == final_conjunction_name
                    )
                    if is_a_high_signal_from_module_to_final_conjunction:
                        name_of_final_conjunction_input_modules_that_sent_a_high_signal.add(module_name)

                new_signal: Signal = destination_module.process_input(signal)
                if new_signal.bit_signal is not None:
                    next_signals.append(new_signal)
        current_signals = next_signals
    return name_of_final_conjunction_input_modules_that_sent_a_high_signal



