from GraphInterface import GraphInterface
from AStarAlgorithm import AStarAlgorithm

filename = "problems/10/instance_3.txt"
g = GraphInterface.fromFile(filename)
a = AStarAlgorithm(g)
no_traversed, path, cost = a.run(max_traversed=999999999999999999)
print(no_traversed)
print(path)
print(cost)
