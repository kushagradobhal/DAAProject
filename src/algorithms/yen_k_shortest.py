import networkx as nx

def shortest_path(graph, start, end, k=1):
    try:
        paths = list(nx.shortest_simple_paths(graph, start, end, weight='weight'))
        if len(paths) >= k:
            path = paths[k-1]
            cost = sum(graph[path[i]][path[i+1]].get('weight', 1) for i in range(len(path)-1))
            return path, cost
        else:
            return None, float('inf')
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, float('inf')
