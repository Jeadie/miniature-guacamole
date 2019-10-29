import numpy as np

HEALTHY_CLASS = "healthy.\n"
COLIC_CLASS = "colic.\n"


def open_data(filename: str) -> np.array:
    csv = np.loadtxt(filename, delimiter=",", usecols=tuple(range(16)))
    with open(filename, "r") as f:
        labels =f.readlines()
    labels = np.array([[1 if (l.split(",")[-1] == COLIC_CLASS) else 0 for l in labels]]).T

    print(csv.shape, labels.shape)
    data = np.concatenate([csv, labels], axis=1 )
    return data

if __name__ == '__main__':
    open_data("horseTest.txt")