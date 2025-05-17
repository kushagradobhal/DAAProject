import networkx as nx

def shortest_path(graph, start, end):
    try:
        path = nx.bidirectional_dijkstra(graph, start, end, weight='weight')[1]
        cost = sum(graph[path[i]][path[i+1]].get('weight', 1) for i in range(len(path)-1))
        return path, cost
    except nx.NetworkXNoPath:
        return None, float('inf')
