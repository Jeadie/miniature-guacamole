# Simulated Annealing

## Usage

To run the annealing programmatically,
```
  from GraphInterface import GraphInterface
  from simulated_annealing import SimulatedAnnealing

  g = GraphInterface.fromFile("problems/problem36")
  a = SimulatedAnnealing(g)

  # Path is final tour from annealing (either due to timeout or stable solution)
  # costs are the per iteration cost of the current tour.
  path, costs = a.run(max_iterations=iterations)
```

There are three ways to run TSPs:
1. Running a single file, `python timing.py <FILENAME>`
2. Running all files for a problem size: `python timing.py <PROBLEM_SIZE>`
3. Running all files for problems less than or equal to a size: `python timing.py <PROBLEM_SIZE> all`
NOTE: For the second two usages to work, the problems folder must be located within this. i.e. 'randTSP/problems/'.
