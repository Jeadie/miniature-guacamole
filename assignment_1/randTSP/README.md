# Travelling Salesman Problem

There are three python files used to implement A* search on TSP:
* GraphInterface.py: Loads a problem and provides an interface for the algorithm to
  query the cities. Also has the precomputed distance data structures needed for the
  heuristic.
* AStarAlgorithm.py: Prepares and runs an A* algorithm. Is responsible for the
  heuristic, successor function, goal checking and search tree traversal.
* timing.py: Utility file used in calculating performance values for problems.


## Example usage (CLI):
There are three ways to run TSPs:
1. Running a single file, `python timing.py <FILENAME>`
2. Running all files for a problem size: `python timing.py <PROBLEM_SIZE>`
3. Running all files for problems less than or equal to a size: `python timing.py <PROBLEM_SIZE> all`
NOTE: For the second two usages to work, the problems folder must be located within this. i.e. 'randTSP/problems/'.

## Example usage (Programmatically):

```
from GraphInterface import GraphInterface
from AStarAlgorithm import AStarAlgorithm

filename = "problems/problem36"
g = GraphInterface.fromFile(filename)
a = AStarAlgorithm(g)
no_traversed, path, cost = a.run(max_traversed=10000000)
```

