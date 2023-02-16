import random;
import matplotlib.pyplot as plt;
import numpy;

from Element import Element;
from Gates import *;
from Signal import SignalValue;

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

def generate_individuals(inputs_number, L, N):
    return [[[random.randint(0, 1) for _ in range(inputs_number)] for _ in range(L)] for _ in range(N)];

def generate_empty_signals_table(all_lines):
    return {line[i]: SignalValue(0) for line in all_lines for i in range(1, len(line))};

def setup_input_values(all_lines):
    top_level_inputs = None;
    if all_lines[0][0] == "TLPINPUTS":
        top_level_inputs = all_lines[0][1:];
        all_lines.pop(0);

    signals = generate_empty_signals_table(all_lines);
    elements_table = [Element(line) for line in all_lines];

    if top_level_inputs == None:
        top_level_inputs = top_level_inputs_extraction(signals, elements_table);

    return top_level_inputs, elements_table;

def number_of_switches_on(t1, t2):
    count = 0;
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            count += 1;
    return count;

def process_individual(workload, all_lines, top_level_inputs, elements_table):
    signals = generate_empty_signals_table(all_lines);
    for i in range(len(top_level_inputs)):
        signals[top_level_inputs[i]].value = workload[i];
    sorted_elements_table = sort_elements(signals, elements_table, top_level_inputs);
    process_elements(signals, sorted_elements_table);
    outputs = outputs_from_signals_extraction(signals, top_level_inputs);
    return list(map(lambda out: outputs[out].value, outputs));

def crossover_from(parent1, parent2, N):
    L = len(parent1[1]);
    all_workloads = [];
    all_workloads.append(parent1[1]);
    all_workloads.append(parent2[1]);

    for _ in range(N-2):
        C = random.randint(0, 1);
        if C == 0:
            first_parent = parent1;
            second_parent = parent2;
        else:
            first_parent = parent2;
            second_parent = parent1;

        workload = [];
        R = random.randint(0, L-1);
        for i in range(0, R):
            workload.append(first_parent[1][i]);
        for i in range(R, L):
            workload.append(second_parent[1][i]);
        all_workloads.append(workload);

    return all_workloads;

def mutate(initial_workloads, m):
    def toggle_bit(bit):
        if bit == 1:
            return 0;
        else:
            return 1;

    for workload in initial_workloads:
        for i in range(len(workload)):
            for j in range(len(workload[i])):
                prob = random.random();
                if prob <= m:
                    workload[i][j] = toggle_bit(workload[i][j]);

    return initial_workloads;

def read_file(filename):
    return [line.lstrip().rstrip().split(" ") for line in open(filename, "r")];

def main(L, N, G, m, all_lines):
    top_level_inputs, elements_table = setup_input_values(all_lines);
    best_in_generation = [];
    individual_workloads = generate_individuals(len(top_level_inputs), L, N);

    for _ in range(G):
        score = [];
        for ind_number in range(len(individual_workloads)):
            t1 = process_individual(individual_workloads[ind_number][0], all_lines, top_level_inputs, elements_table);
            t2 = process_individual(individual_workloads[ind_number][1], all_lines, top_level_inputs, elements_table);
            current_score = number_of_switches_on(t1, t2);
            score.append([[], []]);
            score[ind_number][0] = current_score;
            score[ind_number][1] = individual_workloads[ind_number];

        sorted_score = sorted(score);
        print(list(map(lambda s: s[0], sorted_score)));
        parent1 = sorted_score[-1];
        parent2 = sorted_score[-2];

        best_in_generation.append(parent1[0]);

        individual_workloads = crossover_from(parent1, parent2, N);
        individual_workloads = mutate(individual_workloads, m);

    return best_in_generation;

L = 2;
N = 30;
G = 100;
m = 0.05;
all_lines = read_file("model.txt");

best_in_generation1 = main(L, N, G, m, all_lines);
# best_in_generation2 = main(L, N, G, m, all_lines);
# best_in_generation3 = main(L, N, G, m, all_lines);

plt.figure();
plt.plot(best_in_generation1);
# plt.plot(best_in_generation2);
# plt.plot(best_in_generation3);
plt.title("Genetic Stress Test " + str(G) + " Generations using " + str(L) + " Vectors, " + str(N) + " workloads");
plt.xlabel("Generations");
plt.ylabel("# of switches");
plt.show();
