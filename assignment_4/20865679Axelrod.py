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


