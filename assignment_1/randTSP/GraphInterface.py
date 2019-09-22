import numpy as np
from typing import List
from scipy.spatial import distance

class GraphInterface(object):
    """ Provides an abstraction for algorithms to interact with the underlying data.
    """
    def __init__(self, cities: np.array):
        self.cities = cities

        if cities.ndim != 2 or cities.shape[1] != 2:
            raise ValueError(f"Cities must be a nx2 Numpy array, not {cities.shape}.")

        self.n = cities.shape[0]
        self.dist_matrix = distance.cdist(self.cities, self.cities, "euclidean")

    def reset(self):
        return None

    def problem_size(self):
        return self.n

    def backward_cost(self, path: List[int]):
        cost = 0
        for i in range(len(path)-1):
            cost += self.dist_matrix[path[i], path[i+1]]
        return cost

    def get_possible_nodes(self, path: List[int]) -> List[int]:
        """ Gets the possible nodes that have not been traversed by the path.

        Args:
            path: A list of node indices that have been traversed.
        Returns:
            A list of node indices that exist and not in the path, unordered.
        """
        return list(set(range(self.problem_size())).difference(set(path)))

    @staticmethod
    def fromFile(filename: str) -> object:
        with open(filename) as f:
            data = f.readlines()
        n = int(data[0])
        converted = map(lambda x: (int(x[1]), int(x[2])), map(lambda y: y.split(" "), data[1:]))

        return GraphInterface(np.array(list(converted)))

if __name__ == "__main__":
    print(GraphInterface.fromFile("problems/5/instance_4.txt").cities)
