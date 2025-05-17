import networkx as nx

def save_graph(graph, file_path, format='graphml'):
    if format == 'graphml':
        nx.write_graphml(graph, file_path)
    elif format == 'gexf':
        nx.write_gexf(graph, file_path)
    elif format == 'adjlist':
        nx.write_adjlist(graph, file_path)
    else:
        raise ValueError("Unsupported format.")

def load_graph(file_path, format='graphml'):
    if format == 'graphml':
        return nx.read_graphml(file_path)
    elif format == 'gexf':
        return nx.read_gexf(file_path)
    elif format == 'adjlist':
        return nx.read_adjlist(file_path)
    else:
        raise ValueError("Unsupported format.")
