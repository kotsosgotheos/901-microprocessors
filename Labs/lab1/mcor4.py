import numpy;
import matplotlib.pyplot as plt;

def mcor4(N):
    products = [];
    for _ in range(N+1):
        in1 = numpy.random.choice(2, 1)[0];
        in2 = numpy.random.choice(2, 1)[0];
        in3 = numpy.random.choice(2, 1)[0];
        in4 = numpy.random.choice(2, 1)[0];

        out = in1 or in2 or in3 or in4;
        products.append(out);

    pout = numpy.average(products);
    esw = 2 * pout * (1 - pout);
    print("ESW for N = " + str(N) + " -> " + str(esw));
    return esw;

results = [];
results.append([10, mcor4(N=10)]);
results.append([20, mcor4(N=20)]);
results.append([30, mcor4(N=30)]);
results.append([4147, mcor4(N=4147)]);

results_fig = plt.figure();
for res in results:
    plt.plot(res[0], res[1], color="blue", marker="o", markersize=10);

plt.title("Monte Carlo OR4 Switching Activity (4 Generations)");
plt.xlabel("N");
plt.ylabel("Switching Activity");
plt.show();
