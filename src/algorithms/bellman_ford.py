def shortest_path(graph, start, end):
    distance = {node: float('inf') for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}
    distance[start] = 0

    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1)
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u


    for u, v, data in graph.edges(data=True):
        if distance[u] + data.get('weight', 1) < distance[v]:
            raise ValueError("Graph contains a negative-weight cycle")

 
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]

    if distance[end] == float('inf'):
        return None, float('inf')

    return path, distance[end]
