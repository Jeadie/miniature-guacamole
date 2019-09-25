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


    def set_assignment(self, node, value):
        """Sets the value of a node to """
        x, y = node
        self.assignments_data[x, y] = value

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
        print(f"Set {node} to {value}, see: {self.value_data[x,y]}")

    def remove_value(self, node, value):
        """Sets the value of a node to """
        x,y = node
        self.value_data[x,y,value] = 0


    def get_values_for_node(self, node):
        x, y = node
        # possibilities= list(np.where(self.assignments_data == -1))
        # possibilities = list(np.where(self.value_data[x,y,:] == 1)[0])
        possibilities = list(range(9))
        print(f"Possibilities: {possibilities}.")

        # Get indices with numbers in
        used_x, used_y = np.where(self.assignments_data != -1)
        pairs = [(used_x[i], used_y[i]) for i in range(len(used_x))]
        print(pairs)

        # Filter to only important ones
        # or (i[-1] == y) or ((i[0] // 3 == x // 3) and (i[-1] // 3 == y // 3))

        square = list(filter(lambda i: ((i[0] // 3 == x // 3) and (i[-1] // 3 == y // 3)), pairs))
        rows  = list(filter(lambda i:  (i[-1] == y), pairs))
        columns = list(filter(lambda i: (i[0] == x), pairs))

        pairs_ind = list(zip(*rows+columns+square))

        # Get values from remaining positions
        existing = self.assignments_data[pairs_ind]

        print(possibilities, existing)
        # remove contradicting values from possibilities
        return list(set(possibilities).difference(set(existing)))


    def get_single_solution(self):
        return  self.assignments_data  +1
        # result = np.argmax(self.value_data, axis=-1) + 1
        # result[np.where(self.value_data.sum(axis=-1) > 1)] = 0
        # return result

    def get_free_tiles(self):
        free_x, free_y  = np.where(self.assignments_data == -1)
        return [(free_x[i], free_y[i]) for i in range(len(free_x))]


    def is_complete(self):
        free_x, free_y = np.where(self.assignments_data == -1)
        return len(free_x) == 0
