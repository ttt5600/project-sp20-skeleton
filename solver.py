import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys

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


def solve(G):
    """
       Args:
           G: networkx.Graph

       Returns:
           T: networkx.Graph
       """


    degrees = list((G.degree(G.nodes())))
    degrees.sort(key=lambda i:i[1], reverse=True)

    curr_node = degrees[0][0]

    check_tree = DisjointSet(len(G.nodes))

    result = nx.Graph()
    result.add_node(curr_node)

    while not nx.is_dominating_set(G):
        edge_set = list(G.edges([curr_node]))
        smallest_pairwise_dist = float('inf')
        best_edge = None
        for edge in edge_set:
            if check_tree.find(curr_node) != check_tree.find(edge[1]) and curr_node not in list(result.nodes):
                result.add_node(edge[1])
                result.add_edge(edge[0],edge[1])
                if average_pairwise_distance_fast(result) < smallest_pairwise_dist:
                    best_edge = edge
                result.remove_node(edge[1])
        result.add_node(best_edge[1])
        result.add_edge(best_edge[0], best_edge[1])
        curr_node = best_edge[1]

    return result

def solve(G):
    degrees = list((G.degree(G.nodes())))
    degrees.sort(key=lambda i:i[1], reverse=True)

    curr_node = degrees[0][0]
    result = nx.dominating_set(G,[curr_node])




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
