#import networkx as nx
#import random

#def generate_random_graph(num_nodes=10, edge_prob=0.3, weighted=True, directed=False):
 #   G = nx.DiGraph() if directed else nx.Graph()
  #  G.add_nodes_from(range(num_nodes))
   # 
    #for u in range(num_nodes):
     #   for v in range(u+1, num_nodes):
      #      if random.random() < edge_prob:
       #         weight = random.randint(1, 10) if weighted else 1
        #        G.add_edge(u, v, weight=weight)
         #       if directed:
          #          if random.random() < 0.5:
           #             G.add_edge(v, u, weight=weight)

    #return G

import networkx as nx

def simple_weighted_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        ('A', 'B', 1),
        ('A', 'C', 4),
        ('B', 'C', 2),
        ('B', 'D', 5),
        ('C', 'D', 1),
        ('D', 'E', 3)
    ])
    return G

def negative_weight_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', -3),
        ('C', 'D', 2)
    ])
    return G

def disconnected_graph():
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'),
        ('C', 'D')
    ])
    return G

