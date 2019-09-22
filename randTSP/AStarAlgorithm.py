from datetime import datetime
from typing import List, Optional
import heapq
import sys

from GraphInterface import GraphInterface


class AStarAlgorithm(object):
    """ Class to run an A* search on a graph dataset.

    """

    def __init__(self, graph: GraphInterface):
        self.graph = graph
        graph.reset()
        self.reset()

    def reset(self):
        self.nodes_traversed=0
        self.path_queue = []

        heapq.heappush(self.path_queue, (0 + self.heuristic([0]), [0]))

    def is_at_goal_state(self, path: List[int]) -> bool:
        """ Checks the current path against the goal state.

        Args:
            path: An ordered list of cities.

        Returns:
            True, if this achieves the end goal state, False otherwise.
        """
        return len(set(path)) == self.graph.problem_size()

    def run(self, max_traversed) -> Optional[List[str]]:
        """ Runs the A* search

        Args:
            max_traversed: The number of nodes to traverse before stopping.

        Returns:
            If the algorithm successfully completes, an order list of node names will
            be returned. If the max_traversed was reached, None.
        """

        # Get Node
        while self.nodes_traversed < max_traversed:
            try:
                score, path = heapq.heappop(self.path_queue)
                # print(f"Expanding path with score {score}: {path}.")
            except IndexError:
                print("[ERROR] - Ran out of nodes to traverse.")
                raise

            # Check node is at goal state.
            if self.is_at_goal_state(path):
                return path
            else:
                self.nodes_traversed += 1

            # Get all possible successor paths
            successor_nodes = self.graph.get_possible_nodes(path)
            successor_paths = [path+[node] for node in successor_nodes]

            # Add to priority queue with respect to current_cost + heuristic
            for p in successor_paths:
                value = self.graph.backward_cost(p) + self.heuristic(p)
                heapq.heappush(self.path_queue, (value, p))

        print("[WARNING] - Traversal limit reached.")
        return None


    def heuristic(self, x: List[int]) -> float:
        """ Returns the heuristic value of a path.

        Args:
            x: A list of integers representing the cities of the path, in order.

        Returns:
            A heuristic of how close this path is to the goal state.
        """
        return 0

if __name__ == "__main__":
    n = int(sys.argv[1])
    g = GraphInterface.fromFile(f"problems/{n}/instance_1.txt")
    a = AStarAlgorithm(g)
    start = datetime.now()
    a.run(max_traversed=10000000)
    end = datetime.now()
    print(f"Took, {(end-start).total_seconds()} seconds.")