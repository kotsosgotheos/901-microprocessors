class SignalValue:
    def __init__(self, i):
        self.marked = False;
        self.value = i;

    def mark(self):
        self.marked = True;

    def unmark(self):
        self.marked = False;

    def is_marked(self):
        return self.marked;

    def __str__(self):
        return str(self.value);

## NOTE Assume 1 output gates
# Element("AND", "e", ["a", "b", "c"])
class Element:
    def __init__(self, type, output, inputs):
        self.type = type;
        self.output = output;
        self.inputs = inputs;

def multi_input_of(GATE, inputs):
    res = GATE(inputs[0], inputs[1]);
    for i in range(2, len(inputs)):
        res = GATE(res, inputs[i]);
    return res;

def AND(*inputs):
    AND2 = lambda in1, in2 : in1 * in2;
    return multi_input_of(AND2, inputs);

def OR(*inputs):
    OR2 = lambda in1, in2: 1 - (1 - in1) * (1 - in2);
    return multi_input_of(OR2, inputs);

def XOR(*inputs):
    XOR2 = lambda in1, in2: in1 * (1 - in2) + (1 - in1) * in2;
    return multi_input_of(XOR2, inputs);

def NAND(*inputs):
    return 1 - AND(*inputs);

def NOR(*inputs):
    return 1 - OR(*inputs);

def XNOR(*inputs):
    return 1 - XOR(*inputs);

def NOT(in0):
    return 1 - in0;

def intermediate_esws(outputs):
    return {pout[0]: 2 * pout[1].value * (1 - pout[1].value) for pout in outputs.items()};

def outputs_from_signals_extraction(signals, top_level_inputs):
    return {out[0]: out[1] for out in signals.items() if out[0] not in top_level_inputs};

def top_level_inputs_extraction(signals, elements_table):
    return [sig for sig in signals if sig not in map(lambda e : e.output, elements_table)];

def process_elements(signals, elements):
    def calculate_gate_result(GATE):
        return GATE(*map(lambda i : signals[i].value, e.inputs));

    for e in elements:
        signals[e.output].value = calculate_gate_result(eval(e.type));

def manual_input():
    return list(map(lambda line: line.split(" "), [
        "AND e a b",
        "NOT f c",
        "AND d e f",
    ]));

def read_file(filename):
    return [line.lstrip().rstrip().split(" ") for line in open(filename, "r")];

def sort_elements(signals, unsorted_elements, top_level_inputs):
    def all_inputs_marked(e):
        return all([signals[gate_input].is_marked() for gate_input in e.inputs]);

    sorted_elements = [];

    for key in signals:
        if key in top_level_inputs:
            signals[key].mark();

    while len(sorted_elements) < len(unsorted_elements):
        for e in filter(lambda e : all_inputs_marked(e), unsorted_elements):
            signals[e.output].mark();
            sorted_elements.append(e);

    return sorted_elements;

def setup_input_values(all_lines):
    if all_lines[0][0] == "top_inputs":
        top_level_inputs = all_lines[0][1:];
        all_lines.pop(0);
    else:
        top_level_inputs = None;

    signals = {line[i]: SignalValue(0) for line in all_lines for i in range(1, len(line))};
    elements_table = [Element(line[0], line[1], [i for i in line[2:]]) for line in all_lines];

    if top_level_inputs == None:
        top_level_inputs = top_level_inputs_extraction(signals, elements_table);

    # signals = {"a": SignalValue(0), "b": SignalValue(0), ... }
    # top_level_inputs = ["a", "b", ...]
    # elements_table = [Element("AND", "e", ["a", "b"]), ... ]
    return signals, top_level_inputs, elements_table;

def testbench(all_lines):
    truth_table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]];
    truth_table.append([0.5, 0.5, 0.5]);
    truth_table.append([0.4147, 0.4147, 0.4147]);
    signals, top_level_inputs, elements_table = setup_input_values(all_lines);

    for input_set in truth_table:
        for s in signals:
            signals[s].unmark();
        for i in range(len(top_level_inputs)):
            signals[top_level_inputs[i]].value = input_set[i];

        sorted_elements_table = sort_elements(signals, elements_table, top_level_inputs);
        process_elements(signals, sorted_elements_table);
        outputs = outputs_from_signals_extraction(signals, top_level_inputs);

        if input_set[0] != 0 and input_set[0] != 1:
            esws = intermediate_esws(outputs);
            print("\nCOMPLEX(" + str(signals["a"]) + ", " + str(signals["b"]) + ", " + str(signals["c"]) + ") -> " + str(signals["e"]) + " -> " + str(signals["f"]) + " = \033[38;5;207m" + str(signals["d"]) + "\033[0m, esw(e) = " + str(esws["e"]) + ", esw(f) = " + str(esws["f"]) + ", esw(d) = \033[38;5;207m" + str(esws["d"]) + "\033[0m");
        else:
            print("COMPLEX(" + str(signals["a"]) + ", " + str(signals["b"]) + ", " + str(signals["c"]) + ") -> " + str(signals["e"]) + " -> " + str(signals["f"]) + " = \033[38;5;207m" + str(signals["d"]) + "\033[0m");

print("-------------");
print("testbench 3.1");
testbench(manual_input());

print("-------------");
print("testbench 3.2");
testbench(read_file("sorted_model.txt"));
# testbench(read_file("sorted_model_top.txt"));

print("-------------");
print("testbench 3.3");
testbench(read_file("unsorted_model.txt"));
# testbench(read_file("unsorted_model_top.txt"));
