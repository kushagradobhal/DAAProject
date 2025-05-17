import heapq

def shortest_path(graph, start, end):
    
    pq = [(0, start, [])]  
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]
        if node == end:
            return path, cost

        for neighbor in graph.neighbors(node):
            weight = graph[node][neighbor].get('weight', 1)
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path))

    return None, float('inf')  
