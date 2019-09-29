import os
import sys

from data_loader import SudokuGrid
from backtracking_template import BackTrackingTemplate


def run_sudoku(filename: str, forward_check: bool, heuristics: bool):
    """ Runs a single sudoku problem.

    Args:
        filename: The name of the sudoku file to use.
        forward_check: If True, will use forward checking in heuristic.
        heuristics: If True, will use additional heuristics
    Returns:
        A tuple consisting of:
            0. The solution to the Sudoku (or None if limit reached).
            1. The number of nodes traversed.
    """
    grid = SudokuGrid(filename)
    algorithm = BackTrackingTemplate(grid, forward_check, heuristics)
    return algorithm.run()

def main():
    command = sys.argv[1]
    print(f"Command: {command}")
    if command == "all":
        n = int(sys.argv[2])

        forward = "--forward" in sys.argv
        heuristics = "--heuristics" in sys.argv

        results = {}
        for i in range(1, n+1):
            results[i] = []
            for file in os.listdir(f"problems/{i}/"):
                solution, nodes = run_sudoku(f"problems/{i}/{file}", forward, heuristics)
                results[i].append(nodes)

        for size, nodes in results.items():
            print(f"n={size} Average nodes traversed={sum(nodes)/len(nodes)}. Nodes: {nodes}.")

    elif command == "compare":
        n = int(sys.argv[2])

        for i in range(1, n + 1):
            resultsA = []
            resultsB = []
            resultsC = []

            for file in os.listdir(f"problems/{i}/"):
                solutionA, nodesA = run_sudoku(f"problems/{i}/{file}", False, False)
                solutionB, nodesB = run_sudoku(f"problems/{i}/{file}", True, False)
                solutionC, nodesC = run_sudoku(f"problems/{i}/{file}", True, True)
                resultsA.append(nodesA)
                resultsB.append(nodesB)
                resultsC.append(nodesC)

            # print results online
            print(f"{i}, {sum(resultsA) / len(resultsA)}, {sum(resultsB) / len(resultsB)}, {sum(resultsC) / len(resultsC)}")
            # print(f"n={i} Average nodes A={sum(resultsA) / len(resultsA)}. Average nodes B={sum(resultsB) / len(resultsB)}. Average nodes C={sum(resultsC) / len(resultsC)}")

    elif command == "compare_file":
        filename = sys.argv[2]

        solutionA, nodesA = run_sudoku(filename, False, False)
        solutionB, nodesB = run_sudoku(filename, True, False)
        solutionC, nodesC = run_sudoku(filename, True, True)

        # print results online
        print(f"File: {filename}")
        print(f"Nodes A={nodesA}")
        print(f"Nodes B={nodesB}")
        print(f"Nodes C={nodesC}")


    elif command == "run":
        filename = sys.argv[2]
        forward = "--forward" in sys.argv
        heuristics = "--heuristics" in sys.argv
        solution, nodes = run_sudoku(filename, forward, heuristics)
        print(f"file: {filename}. Nodes traversed={nodes}. Solution:")
        print(solution)


if __name__ == '__main__':
    main()