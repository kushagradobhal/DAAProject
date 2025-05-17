import numpy as np
import random

def get_adjacency_matrix(graph):
    return np.to_numpy_array(graph)

def get_adjacency_list(graph):
    adj_list = {node: list(graph.neighbors(node)) for node in graph.nodes}
    return adj_list


def select_random_nodes(graph):
    nodes = list(graph.nodes)
    if len(nodes) < 2:
        raise ValueError("Graph must have at least 2 nodes.")
    start, end = random.sample(nodes, 2)
    return start, end