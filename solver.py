import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance_fast
import sys
import os
from zipfile import ZipFile 
import re

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

def solve_attempt(G):
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
    queue = [curr_node]
    while not nx.is_dominating_set(G, result):
        edge_set = list(G.edges([curr_node]))
        smallest_pairwise_dist = float('inf')
        best_edge = None
        for edge in edge_set:
            print(edge)
            if check_tree.find(curr_node) != check_tree.find(edge[1]) and edge[1] not in list(result.nodes):
                result.add_node(edge[1])
                result.add_edge(edge[0],edge[1],weight=G.edges[curr_node, edge[1]]['weight'])
                if average_pairwise_distance_fast(result) < smallest_pairwise_dist:
                    best_edge = edge
                result.remove_edge(edge[0],edge[1])
                result.remove_node(edge[1])
        if best_edge:
            result.add_node(best_edge[1])
            result.add_edge(curr_node, best_edge[1], weight=G.edges[curr_node, best_edge[1]]['weight'])
            check_tree.union(curr_node, best_edge[1])
            curr_node = best_edge[1]
        else:
            break

    return result   
    

def solve(G):
    '''Kruskal's Algorithm'''
    edges = list(G.edges.data('weight'))
    edges.sort(key=lambda x: x[2])
    
    result = nx.Graph()

    check_tree = DisjointSet(len(G.nodes))
    
    index = 0
    while not (nx.is_dominating_set(G,result) and nx.is_connected(result)):
        edge = edges[index]
        if check_tree.find(edge[0]) != check_tree.find(edge[1]):
            result.add_node(edge[0])
            result.add_node(edge[1])
            result.add_edge(edge[0],edge[1],weight=edge[2])
            check_tree.union(edge[0],edge[1])
        index+=1
    return result

'''from Geeks for Geeks'''
def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths 

    
if __name__ == '__main__':
    file_paths = get_all_file_paths('./inputs')
    for path in file_paths:
        try:
            p = re.compile(r'(small-([0-9]+)|medium-([0-9]+)|large-[0-9]+)')
            result = p.search(path)
            path_name = result.group(0)
            G = read_input_file(path)
            T = solve(G)
            assert is_valid_network(G, T)
            # print("Average  pairwise distance: {}".format(average_pairwise_distance_fast(T)))

            write_output_file(T, 'out/{}.out'.format(path_name))
        except:
            print("failed")




