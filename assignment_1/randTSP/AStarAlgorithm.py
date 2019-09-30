from datetime import datetime
from typing import List, Optional, Tuple
import heapq
import sys
from string import ascii_uppercase

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
        return len(path) > self.graph.problem_size()

    def run(self, max_traversed=10000000) -> Tuple[int, Optional[List[str]], float]:
        """ Runs the A* search

        Args:
            max_traversed: The number of nodes to traverse before stopping.

        Returns:
            Returns a tuple containing the number of nodes expanded, the solution
            path and the overall cost of the solution. If the algorithm successfully
            completes, an order list of node names
            will be returned. If the max_traversed was reached, None.
        """


        while self.nodes_traversed < max_traversed:
            # Get node with lowest score (either backward cost or backward cost and heuristic).
            try:
                score, path = heapq.heappop(self.path_queue)
            except IndexError:
                print("[ERROR] - Ran out of nodes to traverse.")
                raise

            # If all nodes have been traversed, must consider cost of going back to
            if len(path) == self.graph.n:
                successor_node = path + [0]
                value = self.graph.backward_cost(successor_node)
                heapq.heappush(self.path_queue, (value, successor_node))

            # else add all possible next nodes based on cost, cost+heuristic
            elif len(path) < self.graph.n:
                # Get all possible successor paths
                successor_nodes = self.graph.get_possible_nodes(path)
                successor_paths = [path+[node] for node in successor_nodes]

                # Add to priority queue with respect to current_cost + heuristic
                for p in successor_paths:
                    value = self.graph.backward_cost(p) + self.heuristic(p)
                    heapq.heappush(self.path_queue, (value, p))

            # Check node is at goal state.
            if self.is_at_goal_state(path): # and score <= new_score:
                return (self.nodes_traversed, self.to_letters(path),
                        self.graph.backward_cost(path))
            else:
                self.nodes_traversed += 1

        print("[WARNING] - Traversal limit reached.")
        return (self.nodes_traversed, None)

    def to_letters(self, path):
        """ Converts a path in index form to alphabetical form.

        Args:
            path: An ordered list of indices.

        Returns:
            A list, with same ordering, where indices have been replaced by the
            corresponding letter.
        """
        # Poor way to accomodate for when 26 < len(path) < 52
        values = [x for x in ascii_uppercase]
        values.extend([f"A{i}" for i in ascii_uppercase])
        return [values[i] for i in path]

    def heuristic(self, x: List[int]) -> float:
        """ Returns the heuristic value of a path.

        Args:
            x: A list of integers representing the cities of the path, in order.

        Returns:
            A heuristic of how close this path is to the goal state.
        """
        remaining = self.graph.get_possible_nodes(x)
        distances = self.graph.get_closest_distance([x[-1]] + remaining, remaining + [0])

        #Check for empty lists
        if not(distances) or distances[0] < 0:
            return 0
        else:
            return sum(distances)
