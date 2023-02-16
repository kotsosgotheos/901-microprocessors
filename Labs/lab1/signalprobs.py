def sp_of_2_inputs(in1, in2):
    def display(gate):
        result = gate();
        print("sp2" + gate.__name__ + "(" + str(in1) + ", " + str(in2) + ") = " + str(result) + ", SA = " + str(2 * result * (1 - result)));

    def AND():
        return in1 * in2;

    def OR():
        return 1 - (1 - in1) * (1 - in2);

    def XOR():
        return in1 * (1 - in2) + (1 - in1) * in2;

    def NOR():
        return 1 - OR();

    def NAND():
        return 1 - AND();

    display(AND);
    display(OR);
    display(XOR);
    display(NOR);
    display(NAND);

def sp_of_3_inputs(in1, in2, in3):
    def display(gate):
        result = gate();
        print("sp3" + gate.__name__ + "(" + str(in1) + ", " + str(in2) + ", " + str(in3) + ") = " + str(result) + ", SA = " + str(2 * result * (1 - result)));

    def AND():
        return in1 * in2 * in3;

    def OR():
        return 1 - ((1 - in1) * (1 - in2) * (1 - in3));

    def XOR():
        return in1 * (1 - in2) * (1 - in3) + (1 - in1) * in2 * (1 - in3) + (1 - in1) * (1 - in2) * in3 + (in1 * in2 * in3);

    def NOR():
        return 1 - OR();

    def NAND():
        return 1 - AND();

    display(AND);
    display(OR);
    display(XOR);
    display(NOR);
    display(NAND);

def sp_of_n_inputs(*inputs):
    def display(gate):
        result = gate();
        res = "sp" + str(len(inputs)) + gate.__name__ + "(";
        for i in range(len(inputs) - 1):
            res += str(inputs[i]) + ", ";
        res += str(inputs[-1]) + ") = " + str(result) + ", SA = " + str(2 * result * (1 - result));
        print(res);
    
    def multiple_gates(GATE):
        res = GATE(inputs[0], inputs[1]);
        for i in range(2, len(inputs)):
            res = GATE(res, inputs[i]);
        return res;

    def AND():
        def AND2(in1, in2):
            return in1 * in2;
        return multiple_gates(AND2);

    def OR():
        def OR2(in1, in2):
            return 1 - (1 - in1) * (1 - in2);
        return multiple_gates(OR2);

    def XOR():
        def XOR2(in1, in2):
            return in1 * (1 - in2) + (1 - in1) * in2;
        return multiple_gates(XOR2);

    def NOR():
        return 1 - OR();

    def NAND():
        return 1 - AND();

    display(AND);
    display(OR);
    display(XOR);
    display(NOR);
    display(NAND);

sp_of_2_inputs(0.3, 0.5);
# sp_of_2_inputs(0.5, 0.5);
print("-------");
sp_of_3_inputs(0.5, 0.5, 0.5);
print("-------");
# sp_of_n_inputs(0.5, 0.5, 0.5, 0.5);
sp_of_n_inputs(0.5, 0.25, 0.5, 0.25);
