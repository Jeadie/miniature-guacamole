import os
import sys
from datetime import datetime
from typing import List, Tuple

from GraphInterface import GraphInterface
from AStarAlgorithm import AStarAlgorithm


def int_just(x:float, size:int) -> str:
    """ Formats a number to a string of length size.
    """
    if len(str(x)) > size:

        return str(round(x, size-1-len(str(int(x)))))

    return str(x).ljust(size)

def run_problem_size(n: int, print_individual: bool=True)->List[Tuple[float, float]]:
    """ Runs all problems for a single problem size.

    Args:
        n: The size of problems to consider
    """
    times = []
    nodes = []

    for f in os.listdir(f"problems/{n}/"):
        g = GraphInterface.fromFile(f"problems/{n}/{f}")
        a = AStarAlgorithm(g)
        start = datetime.now()
        count, paths, cost = a.run(max_traversed=10000000)
        end = datetime.now()
        times.append((end - start).total_seconds())
        if print_individual:
            print(f"Problem of Size: {n}. Nodes: {int_just(count, 3)}Time: {int_just((end - start).total_seconds(), 10)}Cost: {int_just(cost, 5)}Solution: {paths}")
        nodes.append(count)
    return (sum(nodes)/float(n), sum(times)/float(n))

def main():
    try:
        n = int(sys.argv[1])


    # Run Single File
    except ValueError:
        g = GraphInterface.fromFile(sys.argv[1])
        a = AStarAlgorithm(g)
        start = datetime.now()
        count, paths, cost = a.run(max_traversed=10000000)
        end = datetime.now()
        print(f"File: {sys.argv[1]}.\nNodes: {count}. \nTime (s): {(end - start).total_seconds()}. \nCost: {int_just(cost,5)} \nSolution: {paths}.")
    else:

        # Run all files for all problems <= argv[1]
        if len(sys.argv) >=3 and sys.argv[2] == "all":
            results = []
            for i in range(1, n + 1):
                a, b = run_problem_size(i, print_individual=False)
                results.append((a, b))

            for t, i in zip(results, range(1, n+1)):
                print(
                    f"Cities: {int_just(i, 3)}Average Nodes Traversed: {int_just(t[0], 6)} Average Time (s): {int_just(t[1], 12)}")

        # Run all files for problems of size argv[1]
        else:
            a, b = run_problem_size(n)
            print(f"\nFor {n} cities. \nAverage Nodes Traversed: {a} \nAverage Time (s): {b}.")


if __name__ == '__main__':
    main()
