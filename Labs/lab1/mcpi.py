import numpy;
import matplotlib.pyplot as plt;

def mcpi(N):
    scatterplot = plt.figure();
    points_inside_circle = 0;
    for _ in range(N + 1):
        x = 1 - 2*numpy.random.random();
        y = 1 - 2*numpy.random.random();
        # if numpy.sqrt(x*x + y*y) <= 1:
        if (x*x + y*y) <= 1:
            plt.plot(x, y, color="green", marker="o", markersize=2);
            points_inside_circle += 1;
        else:
            plt.plot(x, y, color="red", marker="o", markersize=2);

    pi = 4 * points_inside_circle / N;
    print("N = " + str(N) + " -> " + str(pi));
    scatterplot.show();
    return pi;

pis = [];
pis.append([10, mcpi(N=10)]);
pis.append([100, mcpi(N=100)]);
pis.append([1000, mcpi(N=1000)]);
pis.append([4147, mcpi(N=4147)]);
pis.append([10000, mcpi(N=10000)]);

results_fig = plt.figure();
for pi in pis:
    plt.plot(pi[0], pi[1], color="blue", marker="o", markersize=10);

plt.title("Monte Carlo π Approximation (5 generations)");
plt.xlabel("N");
plt.ylabel("π");
plt.xlim([-500, 11000]);
plt.ylim([0, 6]);
plt.show();
