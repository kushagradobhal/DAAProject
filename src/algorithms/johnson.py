import networkx as nx

def shortest_path(graph, start, end):
    try:
        paths = nx.johnson(graph, weight='weight')
        path = paths[start][end]
        cost = sum(graph[path[i]][path[i + 1]].get('weight', 1) for i in range(len(path) - 1))
        return path, cost
    except (nx.NetworkXNoPath, KeyError):
        return None, float('inf')
