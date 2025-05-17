import networkx as nx

def shortest_path(graph, start, end):
    """
    Floyd-Warshall algorithm implementation for finding the shortest path between two nodes.
    
    Args:
        graph: NetworkX graph object
        start: Starting node
        end: Target node
        
    Returns:
        tuple: (path, cost) where path is a list of nodes and cost is the total path cost
    """
    try:
        # Get predecessor matrix and distance matrix
        pred, dist = nx.floyd_warshall_predecessor_and_distance(graph, weight='weight')
        
        # Check if end is reachable from start
        if end not in dist[start]:
            return None, float('inf')
            
        # Try to use nx.reconstruct_path if available
        try:
            path = nx.reconstruct_path(start, end, pred)
        except Exception:
            # Manual path reconstruction fallback
            path = []
            curr = end
            while curr != start:
                path.insert(0, curr)
                if curr not in pred[start]:
                    return None, float('inf')
                curr = pred[start][curr]
            path.insert(0, start)
        return path, dist[start][end]
    except (KeyError, nx.NetworkXNoPath):
        return None, float('inf')
