from collections import deque

def shortest_path(graph, start, end):
    distance = {node: float('inf') for node in graph.nodes}
    in_queue = {node: False for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}

    distance[start] = 0
    queue = deque([start])
    in_queue[start] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for v in graph.neighbors(u):
            weight = graph[u][v].get('weight', 1)
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True

   
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]

    return path if path[0] == start else None, distance[end]
