'''
This Python module models the three-player Prisoner's Dilemma game.
We use the integer "0" to represent cooperation, and "1" to represent 
defection. 

Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where
we give the payoff for the first player in the list. We want the three-player game 
to resemble the 2-player game whenever one player's response is fixed, and we
also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique ordering

U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)

The payoffs for player 1 are given by the following matrix:

@author: akhtsang
Created on Feb 9, 2017
'''

import random
import math

PAYOFF = [[[6, 3], [3, 0]], [[8, 5], [5, 2]]]
NROUNDS = 100


"""
So payoff[i][j][k] represents the payoff to player 1 when the first
player's action is i, the second player's action is j, and the
third player's action is k.

In this simulation, triples of players will play each other repeatedly in a
'match'. A match consists of about 100 rounds, and your score from that match
is the average of the payoffs from each round of that match. For each round, your
strategy is given a list of the previous plays (so you can remember what your 
opponent did) and must compute the next action.
 """


class Player(object):
    """
    This defines an interface for a player of the 3-player.  Inherit and modify this class
    by declaring the following:
    
    class SecretStrategyPlayer(Player)
        # code goes here
        # make sure you implement the play(...) function
    
    Attributes:
    While you are not prohibited from adding attributes.  You should not need 
    to implement do so.  The parameters to play(...) contain all information 
    available about the current state of play. 
    """

    def studentID(self):
        """ Returns the creator's numeric studentID """
        raise NotImplementedError("studentID not implemented")

    def agentName(self):
        """ Returns a creative name for the agent """
        return self.__class__.__name__

    def play(self, myHistory, oppHistory1, oppHistory2):
        """ 
        Given a history of play, computes and returns your next move
        ( 0 = cooperate; 1 = defect )
        myHistory = list of int representing your past plays
        oppHisotry1 = list of int representing opponent 1's past plays
        oppHisotry2 = list of int representing opponent 2's past plays
        NB: use len(myHistory) to find the number of games played
        """
        raise NotImplementedError("play not implemented")


class NicePlayer(Player):
    """
    The nicePlayer always cooperates (plays 0).
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Nice Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return 0


class MeanPlayer(Player):
    """
    The meanPlayer always defects (plays 1).
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Mean Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return 1


class RandomPlayer(Player):
    """
    The randomPlayer chooses an action randomly.
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Random Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return random.randint(0, 1)

class Axelrod(Player):
    """

    """
    DISCOUNT_FACTOR = 0.97
    NOISE_FACTOR = 0.2
    RANDOM_FACTOR = 0.05
    COOPERATE_ROUNDS = 5

    def studentID(self):
        """ Returns the creator's numeric studentID """
        return "20865679"

    def agentName(self):
        """ Returns a creative name for the agent """
        return self.__class__.__name__

    def play(self, myHistory, oppHistory1, oppHistory2):
        """
        Given a history of play, computes and returns your next move
        ( 0 = cooperate; 1 = defect )
        myHistory = list of int representing your past plays
        oppHisotry1 = list of int representing opponent 1's past plays
        oppHisotry2 = list of int representing opponent 2's past plays
        NB: use len(myHistory) to find the number of games played
        """
        if len(myHistory) < Axelrod.COOPERATE_ROUNDS:
            return 0

        mean_1 = float(sum(oppHistory1)) / len(oppHistory1)
        mean_2 = float(sum(oppHistory2)) / len(oppHistory2)

        # Defect if both other players are more likely than random to constantly defect
        if mean_1 >= (1.0-Axelrod.NOISE_FACTOR) and mean_2 >= (1.0-Axelrod.NOISE_FACTOR):
            # Randomly re-cooperate.
            if random.random() >= Axelrod.RANDOM_FACTOR:
                return 1

        # Apply forgiveness, defecting more recently is worse than latter on.
        factors = [Axelrod.DISCOUNT_FACTOR ** i for i in range(len(myHistory))]
        factors.reverse()
        # normalise as to map back to [0,1]
        factor_sum = sum(factors)

        defect_1 = [(1.0/factor_sum)* f*m for f, m in zip(factors, oppHistory1)]
        defect_2 = [(1.0/factor_sum) * f * m for f, m in zip(factors, oppHistory2)]

        # If either agent is still going to defect based on pst history, defect.
        if sum(defect_1) >= (1.0-Axelrod.NOISE_FACTOR ) and sum(defect_2) >= (1.0-Axelrod.NOISE_FACTOR):
            # Randomly re-cooperate.
            if random.random() <= Axelrod.RANDOM_FACTOR:
                return 0
            else:
                return 1

        # else default to cooperate
        return 0


