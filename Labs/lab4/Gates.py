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
