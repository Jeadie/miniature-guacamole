import numpy as np

p_s = None
p_r = None


def construct_transitions(p_s, p_r, s1_transition):
    """

    Args:
        p_s:
        p_r:
        s1_transition: An integer of either 1 or 2. whereby the MDP will move to
        S_2 or S_3 respectively with probability of 0.9.

    Returns:
        A transition matrix for a given action at state S_1.
    """
    transition_prob = np.zeros((5, 5))

    # S1
    transition_prob[0, 0] = 0.1
    transition_prob[0, s1_transition] = 0.9

    # S2
    transition_prob[1, 1] = p_s
    transition_prob[1, 3] = 1 - p_s

    # S3
    transition_prob[2, 2] = 0.1
    transition_prob[2, 4] = p_r
    transition_prob[2, 3] = 0.9 - p_r

    # S4
    transition_prob[3, 3] = 0.1
    transition_prob[3, 0] = 0.9

    # S5
    transition_prob[4, 4] = 0.1
    transition_prob[4, 0] = 0.9

    return transition_prob


def run_value_iteration(p_s=0.1, p_r=0.1):
    """

    Args:
        p_s: Probability of
    :param p_r:
    :return:
    """
    discount = 0.95
    r = np.array([0, 0, 0, 10, -10]).T
    transition_a = construct_transitions(p_s, p_r, 1)
    transition_b = construct_transitions(p_s, p_r, 2)
    epsilon = 0.0001
    v_t1 = r

    s1_a = r[0] + discount * np.sum(transition_a[0] * v_t1)
    s1_b = r[0] + discount * np.sum(transition_b[0] * v_t1)

    v_t = np.zeros((5))
    v_t[0] = max(s1_a, s1_b)
    v_t[1:] = r[1:] + discount * np.sum(transition_a[1:] * v_t1)
    policy = "a" if s1_a > s1_b else "b"

    while np.max(np.abs(v_t - v_t1)) > epsilon:
        print(f"{np.max(np.abs(v_t - v_t1))} <= {epsilon}")
        v_t1 = v_t.copy()
        # compute new v_t for each state.
        s1_a = r[0] + np.sum(discount * transition_a[0] * v_t1)
        s1_b = r[0] + np.sum(discount * transition_b[0] * v_t1)
        if s1_a > s1_b + epsilon:
            policy = "a"
        elif s1_b > s1_a + epsilon:
            policy = "b"
        else:
            policy = "Indifferent"

        v_t[0] = max(s1_a, s1_b)
        v_t[1:] = r[1:] + np.sum(discount * transition_a[1:] * v_t1, axis=1)

    print(f"{np.max(np.abs(v_t - v_t1))} <= {epsilon}")
    print(f"Policy is to select: {policy} at S1.")
    return policy

def main():
    # policy = run_value_iteration(p_s=0.2, p_r=0.01)
    # policy2= run_value_iteration(p_s=0.2, p_r=0.03)
    # policy3 = run_value_iteration(p_s=0.2, p_r=0.018985)
    #
    # print(f"Policies: {policy}, {policy3}, {policy2}")

    policy = run_value_iteration(p_s=0.6, p_r=0.1)
    policy2= run_value_iteration(p_s=0.6, p_r=0.2)
    policy3 = run_value_iteration(p_s=0.6, p_r=0.13762 )
    print(f"Policies: {policy}, {policy3}, {policy2}")

if __name__ == "__main__":
    main()