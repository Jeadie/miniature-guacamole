import os
import sys
from datetime import datetime
from typing import List, Tuple
from multiprocessing import Pool


from GraphInterface import GraphInterface
from simulated_annealing import SimulatedAnnealing


def int_just(x: float, size: int) -> str:
    """ Formats a number to a string of length size.
    """
    if len(str(x)) > size:
        return str(round(x, size - 1 - len(str(int(x)))))

    return str(x).ljust(size)


def run_problem_size(n: int, print_individual: bool = True) -> List[
    Tuple[float, float]]:
    """ Runs all problems for a single problem size.

    Args:
        n: The size of problems to consider
    """
    times = []
    nodes = []

    for f in os.listdir(f"problems/{n}/"):
        g = GraphInterface.fromFile(f"problems/{n}/{f}")
        a = SimulatedAnnealing(g)
        start = datetime.now()
        path, costs = a.run(max_iterations=10000)
        cost = costs[-1]
        end = datetime.now()
        times.append((end - start).total_seconds())
    return (sum(nodes) / float(n), sum(times) / float(n))


def run_tour_size(data):
    tour_size, problems_folder, t, iterations = data
    problem_no_data = []
    for problem_no in range(3, 8):
        for attempt in range(3):
            costs = run_annealing(
                f"{problems_folder}/{tour_size}/instance_{problem_no}.txt", t,
                iterations)
            problem_no_data.append((costs[-1], costs[0]))

    return sum([p[0] for p in problem_no_data]) / 15, sum([p[-1] for p in problem_no_data]) / 15

def temperature_schedule_test(problems_folder: str,
                              temperature_constants: List[float]) -> None:
    """ Performs tests on the temperature schedule for a variety of tour sizes.

    Args:
        problems_folder: The path to the problem folder.
        temperature_constants: A list of temperature constants to experiment with.
    """
    PROCESSES = 5
    iterations = 100000
    temperature_data = []
    for t in temperature_constants:
        tour_size_data = {}
        p = Pool(processes = PROCESSES)
        sizes = list(range(5,15))
        results = p.map(run_tour_size, [(i, problems_folder, t, iterations, ) for i in sizes])
        for size, r in zip(sizes, results):
            tour_size_data[size] = r

        temperature_data.append(tour_size_data)

    for t, c in zip(temperature_data, temperature_constants):
        print(c, t)

def run_annealing(problem_path: str, temperature: float, iterations: int) -> List[
    float]:
    """

    Args:
        problem_path:
        temperature

    Returns:
        A list detailing the costs at each iteration.
    """
    g = GraphInterface.fromFile(problem_path)
    a = SimulatedAnnealing(g, temperature=temperature)
    path, costs = a.run(max_iterations=iterations)
    return costs

# run_large_problem(50, 3000000)
def run_large_problem(temperature: float, iterations: int) -> None:
    """ Runs the simulated annealing on a 36 city problem.

    Args:
        temperature: An annealing constant to use in the model.
        iterations: The number of iterations to run through.
    """
    g = GraphInterface.fromFile("problems/problem36")
    a = SimulatedAnnealing(g, temperature=temperature)
    start = datetime.now()
    path, costs = a.run(max_iterations=iterations)
    print(f"total seconds: {(datetime.now()-start).total_seconds()}")
    with open("big_problem_costs.csv", "w") as f:
        f.write(",".join([str(c) for c in costs]))

    print(f"Max cost was {max(costs)}| Min cost was {min(costs)}.")

def main():
    try:
        n = int(sys.argv[1])

    # Run Single File
    except ValueError:
        g = GraphInterface.fromFile(sys.argv[1])
        a = SimulatedAnnealing(g)
        start = datetime.now()
        paths, costs = a.run(max_iterations=100)
        for c in costs:
            print(c)
        cost = costs[-1]
        end = datetime.now()
        print(f"File: {sys.argv[1]}.\nTime (s): {(end - start).total_seconds()}. \nCost: {int_just(cost,5)} \nSolution: {paths}.")
    else:

        # Run all files for all problems <= argv[1]
        if len(sys.argv) >= 3 and sys.argv[2] == "all":
            results = []
            for i in range(1, n + 1):
                a, b = run_problem_size(i, print_individual=False)
                results.append((a, b))

            for t, i in zip(results, range(1, n + 1)):
                print(
                    f"Cities: {int_just(i, 3)}Average Nodes Traversed: {int_just(t[0], 6)} Average Time (s): {int_just( t[1], 12)}")

        # Run all files for problems of size argv[1]
        else:
            a, b = run_problem_size(n)
            print(
                f"\nFor {n} cities. \nAverage Nodes Traversed: {a} \nAverage Time (s): {b}.")


if __name__ == '__main__':
    run_large_problem(50, 9000000)

    # temperature_schedule_test("./problems", [50])
