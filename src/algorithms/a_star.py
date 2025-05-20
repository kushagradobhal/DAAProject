import heapq
import networkx as nx
import numpy as np

def heuristic(a, b):

    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return np.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    
    return 0

def shortest_path(graph, start, end):

    open_set = [(0 + heuristic(start, end), 0, start, [])] 
    visited = set()
    
  
    g_score = {start: 0}
    
    while open_set:
        est_total, cost, node, path = heapq.heappop(open_set)
        
        if node in visited:
            continue
        visited.add(node)
        
        path = path + [node]
        if node == end:
            return path, cost
            
        for neighbor in graph.neighbors(node):
            if neighbor in visited:
                continue
                
            weight = graph[node][neighbor].get('weight', 1)
            tentative_g_score = g_score[node] + weight
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor, path))
    
    return None, float('inf')
