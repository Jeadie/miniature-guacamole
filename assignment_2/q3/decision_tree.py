from typing import List, Tuple

import numpy as np
import math

from data import open_data

FEATURE_NAMES = [
    "K",
    "Na",
    "CL",
    "HCO3",
    "Endotoxin",
    "Aniongap",
    "PLA2",
    "SDH",
    "GLDH",
    "TPP",
    "Breath rate",
    "PCV",
    "Pulse rate",
    "Fibrinogen",
    "Dimer",
    "FibPerDim"
]

CLASS_NAMES = ["HEALTHY", "COLIC"]


class Node(object):
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


def construct_decision_tree(dataset: np.array) -> List[Tuple[int, float]]:
    """Constructs a classifying decision tree from a dataset.

    Args:
        dataset: A nxm+1 shaped ndarray where n is the number of examples, m the number
        of features for each example. The m+1th column is the corresponding binary label
        for the example, \in {0,1}.

    Returns: A binary tree in a standard list format. The elements in the slice
        2^(n-1)+1 to 2^n correspond to the elements of the nth level of the binary tree.

        Each element is a feature, threshold pair where the feature is the column used
        in this node and the corresponding threshold whereby if x[feature] >= threshold
        then the decision tree should traverse to the right node.
    """
    return construct_decision_tree_recurse(dataset)


def construct_decision_tree_recurse(dataset: np.array) -> Node:
    """The recursive method of constructing a classifying decision subtree from a dataset.

    Args:
        dataset: A nxm+1 shaped ndarray where n is the number of examples, m the number
        of features for each example. The m+1th column is the corresponding binary label
        for the example, \in {0,1}.

    Returns: A binary tree in a standard list format. The elements in the slice
        2^(n-1)+1 to 2^n correspond to the elements of the nth level of the binary tree.

        Each element is a feature, threshold pair where the feature is the column used
        in this node and the corresponding threshold whereby if x[feature] >= threshold
        then the decision tree should traverse to the right node.
    """
    # Leaf Node
    if dataset.shape[0] <= 1.0:
        return Node(dataset[0, -1])

    # Decision Node
    f, threshold = get_max_information(dataset)

    # Create Subtrees
    right_node = construct_decision_tree_recurse(
        dataset[dataset[:, f] >= threshold])
    left_node = construct_decision_tree_recurse(
        dataset[dataset[:, f] < threshold])

    # Append back to Node
    node = Node((f, threshold), left=left_node, right=right_node)
    right_node.parent = node
    left_node.parent = node
    return node


def get_max_information(data: np.array) -> Tuple[int, float]:
    """ Calculates the feature and threshold that would maximum the information gain by
        partitioning the dataset by this binary node.

    Args:
        data: A nxm+1 shaped ndarray where n is the number of examples, m the number
        of features for each example. The m+1th column is the corresponding binary label
        for the example, \in {0,1}.

    Returns: A feature, threshold pair where the feature is the column used
        in this node and the corresponding threshold whereby if x[feature] >= threshold
        then the decision tree should traverse to the right node.
    """
    no_features = data.shape[1]

    # Get best feature to split by
    f_max, I_max, t_max = (0, -1, None)

    for f in range(no_features):
        threshold, I = get_max_feature_information(data, f)
        if I > I_max:
            f_max = f
            I_max = I
            t_max = threshold

    return (f_max, t_max)


def get_max_feature_information(data: np.array, index: int) -> Tuple[float, float]:
    """ For a specific feature, calculate the threshold for maximum information gain
    from the two example subsets.

    Args:
        data: A nxm+1 shaped ndarray where n is the number of examples, m the number
        of features for each example. The m+1th column is the corresponding binary label
        for the example, \in {0,1}.

        index: The feature to split the examples by to maximise information.

    Returns: The threshold for the maximum information gain and the information gain
        for this threshold.
    """
    values = data[:, index].copy()
    values.sort()
    thresholds = values[:-1] + np.diff(values)
    I_max, t_max = (-1, thresholds[0])
    for t in thresholds:
        above = data[:, [index, -1]][data[:, index] >= t]
        below = data[:, [index, -1]][data[:, index] < t]
        I = information_value(np.sum(above[:, -1]), len(above)) + information_value(
            np.sum(below[:, -1]), len(below))
        if I > I_max:
            t_max = t
            I_max = I

    return (t_max, I_max)


def information_value(p: int, l: int) -> float:
    """ Computes the information values for a set of binary values.

    Args:
        p: The number of positive examples.
        l: The number of examples.
    Returns:
        The information value of the set of positive and negative examples.
    """

    x = p / l
    if x == 1.0 or x == 0.0:
        return 0.0
    return -(1.0 * x * math.log2(x)) - (1.0 * (1 - x) * math.log2(1 - x))


def test_decision_tree(filename: str, root: Node) -> float:
    """ Tests a decision tree given a dataset.

    Args:
        filename: The filename of the dataset to load and then test against.
        root: Root node of the constructed decision tree.

    Returns:
        The decimal accuracy of the decision tree against the dataset.
    """
    dataset = open_data(filename)
    correct = test_decision_tree_recurse(dataset, root)
    print(f" {correct} Correct out of {dataset.shape[0]}. {(correct * 100) /
                                                           dataset.shape[0]}%.")


def test_decision_tree_recurse(dataset: np.array, node: Node) -> int:
    """ Recursively test decision subtrees.

    If node is a leaf node, calculate accuracy of remaining subset of dataset against
    this decision. Otherwise split dataset according to threshold and recurse.

    Args:
        dataset: The dataset to test the decision substree against.
        node: Node to run decision tree classification with.

    Returns:
        The number of correct classifications of the dataset
    """
    # Empty branch
    if dataset.shape[0] == 0:
        return 0

    # Leaf Node
    if node.left is None and node.right is None:
        return sum(dataset[:, -1] == node.value)

    # Decision Node
    feature, threshold = node.value

    right = dataset[dataset[:, feature] >= threshold]
    left = dataset[dataset[:, feature] < threshold]

    return test_decision_tree_recurse(left, node.left) + test_decision_tree_recurse(
        right, node.right)


def print_tree(root: Node) -> None:
    """ Prints the tree's value edges so to be imported into GraphViz.

    Args:
        root: Root node of the tree.
    """
    if root.left is None and root.right is None:
        return None

    print(f'"{print_node(root)}" -> "{print_node(root.left)}";')
    print(f'"{print_node(root)}" -> "{print_node(root.right)}";')

    print_tree(root.left)
    print_tree(root.right)


def print_node(node) -> str:
    """ Converts node into user-friendly format.

    Args:
        node: Tree nodes

    Return:
        A user readable string for a node.
    """
    if node.left is None and node.right is None:
        return CLASS_NAMES[int(node.value)]

    f_index, threshold = node.value
    return f"{FEATURE_NAMES[f_index]} >= {threshold}"


if __name__ == "__main__":
    # train
    print("Loading Dataset.")
    dataset = open_data("horseTrain.txt")
    print("")

    print("Constructing Decision Tree")
    tree = construct_decision_tree(dataset)
    print("")

    # Evaluate on train and test sets
    print("Testing Decision tree on training and test datasets.")
    test_decision_tree("horseTrain.txt", tree)
    test_decision_tree("horseTest.txt", tree)
    print("")

    # Print Tree for use in GraphViz.
    print("Saving tree structure to tree.txt")
    print_tree(tree)
    print("DONE")