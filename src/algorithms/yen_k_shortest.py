import networkx as nx

def shortest_path(graph, start, end, k=1):
    """
    Yen's algorithm for finding the K shortest simple paths.
    Note: This implementation uses NetworkX's built-in function which is based on Yen's algorithm.
    
    Args:
        graph: NetworkX graph object
        start: Starting node
        end: Target node
        k: The number of shortest paths to find
        
    Returns:
        list: A list of tuples, where each tuple is (path, cost) for the k shortest paths.
              Returns an empty list if no paths are found.
    """
    paths_with_cost = []
    try:
        
        paths_iterator = nx.shortest_simple_paths(graph, start, end, weight='weight')
        
        
        for i, path in enumerate(paths_iterator):
            if i >= k:
                break
            # Calculate the cost of the path
            cost = sum(graph[path[j]][path[j+1]].get('weight', 1) for j in range(len(path)-1))
            paths_with_cost.append((path, cost))
            
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        
        pass 
        
    
    
    paths = []
    try:
        paths_iterator = nx.shortest_simple_paths(graph, start, end, weight='weight')
        for i, path in enumerate(paths_iterator):
            if i >= k:
                break
            paths.append(path)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        pass 
        
    return paths
