import numpy as np

HEALTHY_CLASS = "healthy.\n"
COLIC_CLASS = "colic.\n"


def open_data(filename: str) -> np.array:
    """ Loads a dataset from file and converts it to a numpy dataset.

    Args:
        filename: Name of file that has csv encoded dataset.

    Returns: Numpy of shape nx m+1 where n is the number of examples, m the number
        of features for each example. The m+1th column is the corresponding binary label
        for the example, \in {0,1}.
    """
    csv = np.loadtxt(filename, delimiter=",", usecols=tuple(range(16)))
    with open(filename, "r") as f:
        labels =f.readlines()
    labels = np.array([[1 if (l.split(",")[-1] == COLIC_CLASS) else 0 for l in labels]]).T

    print(csv.shape, labels.shape)
    data = np.concatenate([csv, labels], axis=1 )
    return data
