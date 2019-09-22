import os
import sys
from datetime import datetime

from GraphInterface import GraphInterface
from AStarAlgorithm import AStarAlgorithm


def run_problem_size(n):
    times = []
    for f in os.listdir(f"problems/{n}/"):
        g = GraphInterface.fromFile(f"problems/{n}/{f}")
        a = AStarAlgorithm(g)
        start = datetime.now()
        a.run(max_traversed=10000000)
        end = datetime.now()
        times.append((end - start).total_seconds())
    return sum(times)/float(n)

def main():
    n = int(sys.argv[1])
    results = []
    for i in range(1, n+1):
        results.append(run_problem_size(i))

    for t, i in zip(results, range(1, n+1)):
        print(i, t)


if __name__ == '__main__':
    main()