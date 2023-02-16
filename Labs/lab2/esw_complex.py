import numpy;
import random;
import matplotlib.pyplot as plt;

def AND2(in1, in2):
    return in1 * in2;

def NOT(in0):
    result = 1 - in0;
    return result;

def mc_complex(N):
    products = [];
    for _ in range(N+1):
        in1 = random.randint(0, 1);
        in2 = random.randint(0, 1);
        in3 = random.randint(0, 1);

        out = AND2(AND2(in1, in2), NOT(in3));
        products.append(out);

    pout = numpy.average(products);
    esw = 2 * pout * (1-pout);
    print("N = " + str(N) + " -> " + str(esw));
    return esw;

def output_AND2(a, b):
    e = AND2(a, b);
    print
    return e;

def output_complex(a, b, c):
    e = AND2(a, b);
    f = NOT(c);
    d = AND2(e, f);
    print("COMPLEX(" + str(a) + ", " + str(b) + ", " + str(c) + ") = " + str(d));
    return [e, f, d];

def workload_esw(circuit, outputs):
    number_of_switches = 0;
    maximum_possible_switches = len(outputs) - 1;
    for i in range(len(outputs) - 1):
        if outputs[i] != outputs[i + 1]:
            number_of_switches += 1;

    pout = number_of_switches / maximum_possible_switches;
    esw = 2 * pout * (1-pout);
    print("----");
    print("Ideal esw of " + str(circuit) + ": " + str(esw));

complex_outputs = [];
and2_outputs = [];
not_outputs = [];
def insert_outputs(outputs):
    and2_outputs.append(outputs[0]);
    not_outputs.append(outputs[1]);
    complex_outputs.append(outputs[2]);

insert_outputs(output_complex(0, 0, 0));
insert_outputs(output_complex(0, 0, 1));
insert_outputs(output_complex(0, 1, 0));
insert_outputs(output_complex(0, 1, 1));
insert_outputs(output_complex(1, 0, 0));
insert_outputs(output_complex(1, 0, 1));
insert_outputs(output_complex(1, 1, 0));
insert_outputs(output_complex(1, 1, 1));

workload_esw("COMPLEX", complex_outputs);
workload_esw("AND2", and2_outputs);
workload_esw("NOT", not_outputs);

print("----");

results = [];
results.append([10, mc_complex(N=10)]);
results.append([100, mc_complex(N=100)]);
results.append([4147, mc_complex(N=4147)]);
results.append([10000, mc_complex(N=10000)]);
results.append([10**5, mc_complex(N=10**5)]);

results_fig = plt.figure();
for res in results:
    plt.plot(res[0], res[1], color="blue", marker="o", markersize=10);

plt.title("Monte Carlo Complex Circuit Switching Activity (3 Generations)");
plt.xlabel("N");
plt.ylabel("Switching Activity");
plt.show();
