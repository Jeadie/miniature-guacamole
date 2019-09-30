import numpy as np
from typing import Dict, List
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
        self.closest_cities = self.construct_closest_cities()

    def construct_closest_cities(self) -> Dict[int, List[int]]:
        """ Constructs a mapping between cities and an ordered list of closest city
            indices.

        Returns:
            A mapping from city indices (int) to an ordered list of city indices
            sorted by increasing order of euclidean distance.
        """
        return dict([(i, list(np.argsort(self.dist_matrix[i,:]))[1:]) for i in range(self.n)])

    def reset(self):
        return None

    def problem_size(self):
        return self.n

    def backward_cost(self, path: List[int])->float:
        """ Calculates the backward cost of a path.

        Args:
            path: A list of city indices.

        Returns:
            The cost of traversing the path.
        """
        cost = 0
        for i in range(len(path)-1):
            cost += self.dist_matrix[path[i], path[i+1]]
        return cost

    def get_closest_distance(self, nodes: List[int], travel_to: List[int]) -> List[float]:
        """ For each node, finds the distance of the closest city of which are also in
            the list of nodes.

        Args:
            nodes: A list of nodes to find closest distances to.
            travel_to: A list of nodes to be considered for travelling towards.

        Returns:
            A list, in the respective order, of the distance to the closest city in
            the list of nodes for each node in the list.
        """
        # Sort closest city (in those allowed in travel_to) for each node
        filtered_cities = list(map(lambda x: [c for c in self.closest_cities[x] if c in travel_to], nodes))

        # Return distance to closest city for each node.
        return [self.dist_matrix[x[0], i] if len(x) > 0 else -1 for (x, i) in zip(filtered_cities, nodes)]

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
        converted = map(lambda x: (int(x[1]), int(x[2])), map(lambda y: y.split(" "), data[1:]))

        return GraphInterface(np.array(list(converted)))

if __name__ == "__main__":
    print(GraphInterface.fromFile("problems/5/instance_4.txt").cities)
