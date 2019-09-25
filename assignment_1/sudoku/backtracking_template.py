from typing import Callable, List, Tuple
from data_loader import SudokuGrid
import random
import numpy as np


class BackTrackingTemplate(object):

    def __init__(self, initial_grid: SudokuGrid, forward_checking: bool, heuristic: bool):
        self.grid = initial_grid
        self.forward = forward_checking
        self.heuristic = heuristic


    def run(self, max_steps=10000) -> Tuple[List[List[int]], int]:
        """ Runs the BackTracking Algorithm over the given problem.

        Args:
            max_steps: Number of steps to take in

        Returns:
            A (solution steps) tuple where the solution is a complete Sudoku grid and
            steps is how many partial/complete assignments it had to take,
        """
        self.nodes_traversed = 0
        try:
            return (self.run_recursive(), self.nodes_traversed)
        except AttributeError as e:
            print(e)
            print("Search reached over 10,000 nodes.")
            return (None, self.nodes_traversed)


    def run_recursive(self):
        if self.nodes_traversed > 10000:
            raise AttributeError()

        # Check recursion has worked.
        if self.grid.is_complete():
            return self.grid.get_single_solution()

        # TODO: Add end recurse checking and solution is done checking
        # Get node to traverse,
        self.nodes_traversed += 1
        node = self.select_next_variable(mrv=self.heuristic, mcv=self.heuristic)


        values = self.grid.get_values_for_node(node)
        if len(values) == 0:
            print(self.grid.get_single_solution())
            return None
        else:
            print(values)
        # Perform least constraining ordering.
        # if self.heuristic:
        #     values = self.least_constraining_ordering(values, node)

        # try each value possible
        for v in values:
            # Set value
            # self.grid.set_value(node, v)
            self.grid.set_assignment(node, v)

            # If forward check is used check forward, and if no solution is possible,
            # don't recurse forward.
            # if self.forward and self.forward_check(arc_consistency=self.heuristic):
            #     continue

            # and try subproblem (i.e. recurse down search tree).
            result = self.run_recursive()

            # If that path has solution, return
            if result is not None:
                print("RESULTSULTUSLTUSLTUSTLUSTUL")
                return result

            self.grid.remove_assignment(node)
            # self.grid.remove_value(node, v)

        # If all subtrees cannot be solved, backtrack
        #TODO change back to values for future forward checking
        # print(f"Removing Values {values} setting to node: {node}.")

        self.grid.set_value(node, values)
        print(node, values)
        print(self.grid.get_single_solution())
        return None


    def forward_check(self, arc_consistency):
        """ Checks if, given the current sudoku placements, it is impossible to attain a solution.

        :param arc_consistency:
        Returns:
            True if a solution is not possible, false otherwise (solution is possible or indeterminable)
        """
        return False

    def least_constraining_ordering(self, values, node):
        """ Orders the values to search in increasing order of constraining value.

        Args:
            values: An list of possible values for a node.
            node: The node to have value assigned
        Return:
        The list of values, ordered by their constraining factor.
        """
        return values

    def select_next_variable(self, mrv: bool, mcv: bool) -> Tuple[int]:
        """ Selects the next variable to assign a value to.

        Args:
            mrv: Whether the most restricted variables heuristic should be used.
            mcv: Whether the most constraining variable heuristic should be used for tie-breaking
        Returns:
            The variable in the grid which should be traversed next.
        """
        return self.grid.get_free_tiles()[0]
        # return random.choice(self.grid.get_free_tiles())


if __name__ == '__main__':
    s = SudokuGrid("problems/10/3.sd")
    a = BackTrackingTemplate(s, False, False)
    print(a.run())