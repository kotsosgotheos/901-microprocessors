## NOTE Assume 1 output gates
# Element("AND", "e", ["a", "b", "c"])
class Element:
    def __init__(self, line):
        self.type = line[0];
        self.output = line[1];
        self.inputs = [i for i in line[2:]];
    
    def __str__(self):
        res = self.type + "(";
        for i in range(len(self.inputs) - 1):
            res += self.inputs[i] + ", ";
        res += self.inputs[-1] + ") = " + self.output;
        return res;
