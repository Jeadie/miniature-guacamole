import sys

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
        self.grid.nodes_assigned = 0
        try:
            return (self.run_recursive(), self.grid.nodes_assigned)
        except AttributeError as e:
            # print("Search reached over 10,000 nodes.")
            return (None, self.grid.nodes_assigned)


    def run_recursive(self):
        if self.grid.nodes_assigned> 10000:
            raise AttributeError()

        # Check recursion has worked.
        if self.grid.is_complete():
            return self.grid.get_single_solution()

        # TODO: Add end recurse checking and solution is done checking
        # Get node to traverse,
        node = self.select_next_variable(mrv=self.heuristic, mcv=self.heuristic)


        values = self.grid.get_values_for_node(node)
        if len(values) == 0:
            return None

        # Perform least constraining ordering.
        if self.heuristic:
            values = self.least_constraining_ordering(values, node)

        # try each value possible
        for v in values:
            # Set value
            self.grid.set_assignment(node, v)

            # If forward check is used check forward, and if no solution is possible,
            # don't recurse forward.
            if self.forward:
                constrained_nodes = self.grid.add_variable_constraint(node, v)
                if self.forward_check(arc_consistency=self.heuristic):
                    self.grid.remove_variable_constraint(constrained_nodes, v)
                    self.grid.remove_assignment(node)
                    continue

            # and try subproblem (i.e. recurse down search tree).
            result = self.run_recursive()

            # If that path has solution, return
            if result is not None:
                return result

            # remove forward check constrains on variables now that this assignment does not work.
            if self.forward:
                self.grid.remove_variable_constraint(constrained_nodes, v)

            self.grid.remove_assignment(node)

        # If all subtrees cannot be solved, backtrack
        #TODO change back to values for future forward checking
        # print(f"Removing Values {values} setting to node: {node}.")

        if self.forward:
            self.grid.set_value(node, values)
        return None


    def forward_check(self, arc_consistency):
        """ Checks if, given the current sudoku placements, it is impossible to attain a solution.

        Args:
            arc_consistency: Whether arc consistency should be checked.
        Returns:
            True if a solution is not possible, false otherwise (solution is possible or indeterminable)
        """

        free = self.grid.get_free_tiles()
        for point in free:
            if self.grid.value_data[point[0], point[1]].sum() == 0:
                return True

        if arc_consistency:
            return not self.check_arc_consistency(free)
        else:
            return False

    def check_arc_consistency(self, points):
        """ Checks whether there is arc consistency in the remaining variables to be assigned.

        Args:
            points: A list of (x,y) points without an assignment.
        Return:
            True if there is arc consistency (and thus a possible solution), False otherwise.
        """
        return True

    def least_constraining_ordering(self, values, node):
        """ Orders the values to search in increasing order of constraining value.

        Args:
            values: An list of possible values for a node.
            node: The node to have value assigned
        Return:
        The list of values, ordered by their constraining factor.
        """
        x,y = node

        #Get all free variables on the node's row, column and square.
        free_x, free_y = np.where(self.grid.assignments_data == -1)
        free_points = [(free_x[i], free_y[i]) for i in range(len(free_x))]
        affected = list(filter(lambda i: ((i[0] // 3 == x // 3) and (i[-1] // 3 == y // 3)) or (
                        i[-1] == y) or (i[0] == x), free_points))
        values_remaining = self.    grid.value_data[list(zip(*affected))]

        # how many squares can put the value in its square
        values_count = np.sum(values_remaining, axis = 0)[values]
        values = list(zip(values, values_count))

        # sort values by occurences
        values.sort(key= lambda x: x[-1])
        return [v[0] for v in values]

    def select_next_variable(self, mrv: bool, mcv: bool) -> Tuple[int]:
        """ Selects the next variable to assign a value to.

        Args:
            mrv: Whether the most restricted variables heuristic should be used.
            mcv: Whether the most constraining variable heuristic should be used for tie-breaking
        Returns:
            The variable in the grid which should be traversed next.
        """
        if mrv:
            # get free variables
            free_x, free_y = np.where(self.grid.assignments_data == -1)

            # get number of free values
            values_remaining = np.sum(self.grid.value_data[free_x, free_y], axis=-1)

            # Get minimum
            minimums = np.where(values_remaining == np.amin(values_remaining))[0]


            # tiebreak with most constraining variable
            if len(minimums) > 1 and mcv:
                # Most constraining is variable with least number of assigned variables in its row, column and square.
                free_points = [(free_x[i], free_y[i]) for i in range(len(free_x))]
                min_point = None
                min_value = 100
                for m in minimums:
                    x, y = free_x[m], free_y[m]
                    affected = len(list(filter(lambda i: ((i[0] // 3 == x // 3) and (i[-1] // 3 == y // 3)) or (i[-1] == y) or (i[0] == x), free_points)))

                    if affected > 0:
                        min_value = affected
                        min_point = (x, y)
                return min_point

            # Else just return first element
            else:
                return (free_x[minimums[0]], free_y[minimums[0]])

        # Default, get tiles in order.
        else:
            return self.grid.get_free_tiles()[0]

