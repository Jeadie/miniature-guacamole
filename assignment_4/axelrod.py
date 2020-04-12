from prison import Player
from runTournament import noiseFactor

class Axelrod(Player):
    """

    """
    DISCOUNT_FACTOR = 0.99
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

        mean_1 = float(sum(oppHistory1)) / len(oppHistory1)
        mean_2 = float(sum(oppHistory2)) / len(oppHistory2)


        # Defect if both other players are more likely than random to constantly defect
        if mean_1 >= (1.0-noiseFactor) and mean_2 >= (1.0-noiseFactor):
            return 1

        # Apply forgiveness, defecting more recently is worse than latter on.
        factors = [Axelrod.DISCOUNT_FACTOR ** i for i in range(len(mean_2))]
        factors.reverse()
        # normalise as to map back to [0,1]
        factor_sum = len(factors) / sum(factors)

        defect_1 = [(1.0/factor_sum)* f*m for f, m in zip(factors, mean_1)]
        defect_2 = [(1.0/factor_sum) * f * m for f, m in zip(factors, mean_2)]

        # If either agent is still going to defect based on pst history, defect.
        if mean_1 >= (1.0-noiseFactor) or mean_2 >= (1.0-noiseFactor):
            return 1

        # else default to cooperate
        return 0
