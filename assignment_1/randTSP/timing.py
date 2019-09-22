import os
import sys
from datetime import datetime

from GraphInterface import GraphInterface
from AStarAlgorithm import AStarAlgorithm


def run_problem_size(n):
    times = []
    nodes = []

    for f in os.listdir(f"problems/{n}/"):
        g = GraphInterface.fromFile(f"problems/{n}/{f}")
        a = AStarAlgorithm(g)
        start = datetime.now()
        count, paths = a.run(max_traversed=10000000)
        end = datetime.now()
        times.append((end - start).total_seconds())
        print(f"Complete: {n}, {count}, {(end - start).total_seconds()}.")
        nodes.append(count)
    return (sum(nodes)/float(n), sum(times)/float(n))

def main():
    n = int(sys.argv[1])
    results = []
    a, b = run_problem_size(n)

    # for i in range(1, n+1):
    #     a,b = run_problem_size(i)
    #
    #     # Print to latex table format
    #     print("\hline")
    #     print(f"{i} & {a} & {b} \\\\")
    #     results.append((a,b))

    for t, i in zip(results, range(1, n+1)):
        print(f"{i}, {t[0]}, {t[1]}")


if __name__ == '__main__':
    main()