from datetime import datetime
from typing import List, Optional, Tuple
import heapq
import random
import math

from string import ascii_uppercase

from GraphInterface import GraphInterface


class SimulatedAnnealing(object):
    """ Class to run an A* search on a graph dataset.

    """
    TEMPERATURE_CONSTANT = 50
    STOPPAGE_VALUE = 0.00001

    def __init__(self, graph: GraphInterface, temperature=TEMPERATURE_CONSTANT):
        self.graph = graph
        graph.reset()
        self.reset()
        self.max = 0
        self.temperature = temperature

    def reset(self):
        self.state = list(range(self.graph.n))
        random.shuffle(self.state)
        self.costs = [self.graph.solution_cost(self.state)]

    def run(self, max_iterations=100) -> Tuple[List[str], List[float]]:
        """ Runs the A* search

        Args:
            max_traversed: The number of nodes to traverse before stopping.

        Returns:
            Returns a tuple containing the number of nodes expanded, the solution
            path and the overall cost of the solution. If the algorithm successfully
            completes, an order list of node names
            will be returned. If the max_traversed was reached, None.
        """


        for i in range(max_iterations):
            # Generate Moveset
            moves = self.generate_moveset(self.state)

            if len(moves) == 0:
                return (self.state, self.costs)

            # Choose S i randomly from Moveset(S)
            m = random.choice(moves)

            # Define dV=V(S i )-V(S)
            v_s = self.graph.solution_cost(self.state)
            v_m = self.graph.solution_cost(m)
            dV = v_s - v_m

            # If dV>0 then S←S i else with probability p, S←S i
            if dV > 0 or (random.random() <= self.generate_p(dV)):
                self.state = m
                self.costs.append(v_m)
                self.decrease_temperature( i/max_iterations)
            else:
                self.costs.append(v_s)
                # If downhill descent is minimal, terminate
                if abs(dV/v_s) < SimulatedAnnealing.STOPPAGE_VALUE:
                    return (self.state, self.costs)

        return (self.state, self.costs)

    def generate_p(self, dV: float) -> float:
        """ Generates the probability of making a bad move based on the annealing
            schedule.

        Args:
            dV: The difference between the current and other path's cost.
            t: The fraction of time through the annealing schedule, [0,1]

        Returns:
            A value p \in [0,1] that gives the probability of accepting a worse move.
        """
        return math.exp(dV/self.temperature)

    def decrease_temperature(self, t: float):
        """ Decreases the temperature of the Boltzmann's Constant after taking a worse
            state.

            Args:
                t: The decimal fraction
        """
        # Option A
        # adjustment = 0.9


        # Option B
        adjustment = (1-t)

        # # Option C
        # if self.costs[-1] > self.max:
        #     self.max = self.costs[-1]
        #
        # adjustment = self.costs[-1] / self.max

        self.temperature = self.temperature * adjustment


    def generate_moveset(self, path: List[int]) -> List[List[int]]:
        """ Generates all adjacent movesets from the current path.

        Args:
            path: A complete and valid path.

        Returns:
            A list of possible paths, which are considered neighbours of the current path.
        """
        moves = []
        for i in range(len(path)-1):
            moves.append(path[:i] + [path[i+1], path[i]] + path[i+2:])

        #Easier to deal with last case separately
        if len(moves) > 1:
            moves.append(path[:-2] + [path[-1], path[-2]])
        return moves

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