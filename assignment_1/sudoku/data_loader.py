from typing import List, Tuple
import numpy as np


class SudokuGrid(object):

    def __init__(self, filename):
        with open(filename, "r") as f:
            rows = f.readlines()

            # rows = rows[:9]
            self.value_data = np.array([[int(x) for x in row.split(" ")[:-1]] for row in rows[:-1]])
            self.assignments_data = np.copy(self.value_data) -1
            # Transform to 3D binary where depth has 0,8 one hot if that square can be
            # that value. 0 -> cannot be that value. If singular value in depth, then
            # it is a constant.
            self.value_data = (np.arange(9) == self.value_data[..., None] - 1).astype(int)
            self.value_data[(self.value_data == 0).all(axis=-1), :] =  np.ones((9,9,9))[(self.value_data == 0).all(axis=-1), :]
            self.nodes_assigned = 0
            self.load_initial_variable_constraints()

    def set_assignment(self, node, value):
        """Sets the value of a node to """
        x, y = node
        self.assignments_data[x, y] = value
        self.nodes_assigned +=1

    def remove_assignment(self, node):
        """Sets the value of a node to """
        x,y = node
        self.assignments_data[x,y] = -1

    def set_value(self, node, value):
        """Sets the value of a node to """
        x, y = node
        n_v = np.zeros(9)
        n_v[value] = 1
        self.value_data[x, y] = n_v

    def remove_value(self, node, value):
        """Sets the value of a node to """
        x,y = node
        self.value_data[x,y,value] = 0


    def get_values_for_node(self, node: Tuple[int,int])-> List[int]:
        """ For an unassigned square in the sudoku, return all values still possible
        for assignment.

        Args:
            node: An x,y co-ordinate of a sudoku square (indexed 0-8)

        Returns:
            A list of values that could be assigned to the node.
        """
        x, y = node

        # Get values remaining from forward checking.
        possibilities = list(np.where(self.value_data[x,y,:] == 1)[0])

        # Get co-ordinates of squares already assigned.
        used_x, used_y = np.where(self.assignments_data != -1)
        pairs = [(used_x[i], used_y[i]) for i in range(len(used_x))]

        # get square that would constrain the current node.
        square = list(filter(lambda i: ((i[0] // 3 == x // 3) and (i[-1] // 3 == y // 3)), pairs))
        rows  = list(filter(lambda i:  (i[-1] == y), pairs))
        columns = list(filter(lambda i: (i[0] == x), pairs))
        pairs_ind = list(zip(*rows+columns+square))

        # Get values from remaining positions
        existing = self.assignments_data[pairs_ind]

        # remove contradicting values from possibilities
        return list(set(possibilities).difference(set(existing)))


    def get_single_solution(self)-> List[List[int]]:
        """ Convert solution from [0,8] to [1,9] indexing.

        Returns: A sudoku solution with indexing [1,9].
        """
        return  self.assignments_data  +1

    def get_free_tiles(self)-> List[Tuple[int, int]]:
        """ Returns a list of co-ordinates of squares in the Sudoku without an
            assignment.
        """
        free_x, free_y  = np.where(self.assignments_data == -1)
        return [(free_x[i], free_y[i]) for i in range(len(free_x))]


    def is_complete(self)-> bool:
        """Returns True if the Sudoku is complete.
        """
        free_x, free_y = np.where(self.assignments_data == -1)
        return len(free_x) == 0

    ## FORWARD CHECKING FUNCs
    def load_initial_variable_constraints(self):
        """ Load forward checking from pre-existing variable-value assignments.
        """
        free_x, free_y = np.where(self.assignments_data > -1)
        for x, y in zip(free_x, free_y):
            self.add_variable_constraint((x,y), self.assignments_data[x,y])


    def remove_variable_constraint(self, nodes: List[Tuple[int, int]], value: int):
        """ Removes the forward checking variable constraint on unassigned nodes.

        Args:
            nodes: A list of unassigned nodes.
            value: The value to remove the forward constraint from for each node.
        """
        self.value_data[list(zip(*[(x,y, value) for x,y in nodes]))] = 1

    def add_variable_constraint(self, node:Tuple[int], value:int)-> List[Tuple[int]]:
        """ Adds forward checking constraints to all nodes incident (square, column
            and row) by removing their ability to be the value

        Args:
            node: The node which has been assigned value.
            value: The value the node has been assigned.

        Returns:
            A list of nodes that have been constrained because of this assignment.
        """
        x, y = node
        effected = []
        effected.extend([(i, y, value) for i in range(9)])
        effected.extend([(x, i, value) for i in range(9)])
        x_c, y_c = [(x//3 *3) + i for i in range(3)], [(y//3 *3) + i for i in range(3)]

        for i in x_c:
            for j in y_c:
                effected.append((i,j, value))

        effected.remove((x,y, value))
        # Worry about unassigned variables only
        effected = list(filter(lambda i: self.assignments_data[i[0], i[1]] == -1, effected))

        effected = list(zip(*effected))
        self.value_data[effected] = 0
        return [(x,y) for x,y,z in zip(*effected)]
