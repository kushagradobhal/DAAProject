import networkx as nx

def shortest_path(graph, start, end):
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Graph is not a DAG")

    distance = {node: float('inf') for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}
    distance[start] = 0

    for u in nx.topological_sort(graph):
        for v in graph.successors(u):
            weight = graph[u][v].get('weight', 1)
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u

    path = []
    current = end
    while current:
        path.insert(0, current)
        current = predecessor[current]

    return path if path[0] == start else None, distance[end]
