import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys



def solve(G):
    """
       Args:
           G: networkx.Graph

       Returns:
           T: networkx.Graph
       """

    class DisjointSet:
        def __init__(self, vertices):
            self.vertices = [[v, 0] for v in range(vertices)]

        def contains(self, vertex):
            return vertex in [x[0] for x in self.vertices]

        def find(self, x):
            if x != self.vertices[x][0]:
                self.vertices[x][0] = self.find(self.vertices[x][0])
            return self.vertices[x][0]

        def union(self, x, y):
            rootx = self.find(x)
            rooty = self.find(y)
            if self.vertices[rootx][1] > self.vertices[rooty][1]:
                self.vertices[rooty][0] = rootx
            else:
                self.vertices[rootx][0] = rooty
                if self.vertices[rootx][1] == self.vertices[rooty][1]:
                    self.vertices[rooty][1] += 1

    degrees = list((G.degree(G.nodes())))
    degrees.sort(key=lambda i:i[1], reverse=True)

    max_degree = degrees[0][0]

    check_tree = DisjointSet(len(G.nodes))


    # avg_edgeweights = 0
    # node = 0
    # for i in range(len(G.nodes)):
    #     total = 0
    #     for j in range(len(list(G.edges([i])))):
    #         total += G.edges[list(G.edges([i]))[j]]['weight']
    #     if total > max_edgeweights:
    #         max_edgeweights = total

    # order.sort(key=lambda x: x[1],reverse=True)
    # seen = set()
    # tree = nx.Graph()
    # k = 0
    # while len(seen) != len(G.nodes) and nx.is_connected(tree):
    #     node = order[k][0]
    #     for vertex in list(G.adj[node]):
    #         seen.add(vertex)






# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
