from typing import List, Union, Set


class Signal:
    def __init__(self, source_module, bit_signal, destination_modules):
        self.source_module = source_module
        self.bit_signal: Union[int, None] = bit_signal
        self.destination_modules: List = destination_modules

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Signal(source={self.source_module}, bit={self.bit_signal}, destination={self.destination_modules})"


class DummyModule:
    def __init__(self, name):
        self.name = name
        self.state = 0
        self.output_modules: List[DummyModule] = []
        self.input_modules: List[str] = []

    def process_input(self, signal: Signal):
        return Signal(self, None, [])

    def add_input_module(self, module_name: str):
        self.input_modules.append(module_name)


class BroadCaster:
    def __init__(self):
        self.name = "broadcaster"
        self.state = 0
        self.output_modules: List[DummyModule] = []
        self.input_modules: List[str] = []

    def process_input(self, signal: Signal):
        return Signal(self, 0, self.output_modules)

    def add_output_module(self, module):
        self.output_modules.append(module)


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.state = 0
        self.output_modules: List[DummyModule] = []
        self.input_modules: Set[str] = set()

    def process_input(self, signal: Signal):
        if signal.bit_signal == 1:
            return Signal(self, None, [])
        self.state = 1 - self.state
        return Signal(self, self.state, self.output_modules)

    def add_input_module(self, module_name: str):
        self.input_modules.add(module_name)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"FlipFlop(n={self.name}, s={self.state}, o={self.output_modules})"


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.state = 0
        self.input_module_name_to_index_map = {}
        self.output_modules: List[DummyModule] = []
        self.input_modules: Set[str] = set()

    def update_state(self, signal: Signal):
        shift_amount = self.input_module_name_to_index_map[signal.source_module.name]
        mask = 1 << shift_amount
        shifted_input_signal = signal.bit_signal << shift_amount
        self.state = (self.state & ~mask) | (shifted_input_signal & mask)

    def get_output_bit(self):
        output_signal = 1
        for i in range(len(self.input_module_name_to_index_map)):
            output_signal &= ((self.state >> i) & 1)
        return (~output_signal) & 1

    def process_input(self, signal: Signal):
        self.update_state(signal)
        return Signal(self, self.get_output_bit(), self.output_modules)

    def add_input_module(self, module_name: str):
        if module_name not in self.input_module_name_to_index_map:
            self.input_module_name_to_index_map[module_name] = len(self.input_module_name_to_index_map)
            self.input_modules.add(module_name)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Conjunction(n={self.name}, s={self.state}, o={self.output_modules})"