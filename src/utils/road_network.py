import osmnx as ox
import networkx as nx
from typing import Tuple, Optional, List
import numpy as np
from tqdm import tqdm

class RoadNetworkLoader:
    """
    Class for loading and processing road network data from OpenStreetMap.
    """
    
    def __init__(self):
        self.graph = None
        self.undirected_graph = None
    
    def load_place(self, place: str, network_type: str = 'drive') -> nx.DiGraph:
        """
        Load road network for a specific place.
        
        Args:
            place: Name of the place (e.g., "Dehradun, India")
            network_type: Type of network ('drive', 'walk', 'bike', 'all')
            
        Returns:
            NetworkX DiGraph object
        """
        try:
            self.graph = ox.graph_from_place(place, network_type=network_type)
            return self.graph
        except Exception as e:
            print(f"Error loading place {place}: {str(e)}")
            return None
    
    def load_bbox(self, bbox: Tuple[float, float, float, float], network_type: str = 'drive') -> nx.DiGraph:
        """
        Load road network for a bounding box.
        
        Args:
            bbox: Tuple of (north, south, east, west) coordinates
            network_type: Type of network ('drive', 'walk', 'bike', 'all')
            
        Returns:
            NetworkX DiGraph object
        """
        try:
            self.graph = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type=network_type)
            return self.graph
        except Exception as e:
            print(f"Error loading bbox {bbox}: {str(e)}")
            return None
    
    def simplify_graph(self, tolerance: float = 0.001) -> nx.DiGraph:
        """
        Simplify the graph by removing unnecessary nodes and edges.
        
        Args:
            tolerance: Simplification tolerance
            
        Returns:
            Simplified NetworkX DiGraph
        """
        if self.graph is None:
            return None
        
        self.graph = ox.simplify_graph(self.graph, tolerance=tolerance)
        return self.graph
    
    def create_undirected_graph(self) -> nx.Graph:
        """
        Create an undirected version of the graph.
        
        Returns:
            NetworkX Graph object
        """
        if self.graph is None:
            return None
        
        self.undirected_graph = self.graph.to_undirected()
        return self.undirected_graph
    
    def get_random_nodes(self, num_pairs: int = 1) -> List[Tuple[int, int]]:
        """
        Get random pairs of nodes for testing.
        
        Args:
            num_pairs: Number of node pairs to generate
            
        Returns:
            List of (start, end) node pairs
        """
        if self.graph is None:
            return []
        
        nodes = list(self.graph.nodes())
        pairs = []
        
        for _ in range(num_pairs):
            start = np.random.choice(nodes)
            end = np.random.choice(nodes)
            while end == start:
                end = np.random.choice(nodes)
            pairs.append((start, end))
        
        return pairs
    
    def get_farthest_nodes(self, num_pairs: int = 1) -> List[Tuple[int, int]]:
        """
        Get pairs of nodes that are far apart in the graph.
        
        Args:
            num_pairs: Number of node pairs to generate
            
        Returns:
            List of (start, end) node pairs
        """
        if self.graph is None:
            return []
        
        nodes = list(self.graph.nodes())
        pairs = []
        
        for _ in range(num_pairs):
            # Start with a random node
            start = np.random.choice(nodes)
            
            # Find the farthest node using Dijkstra's algorithm
            distances = nx.single_source_dijkstra_path_length(self.graph, start)
            end = max(distances.items(), key=lambda x: x[1])[0]
            
            pairs.append((start, end))
        
        return pairs
    
    def get_graph_stats(self) -> dict:
        """
        Get statistics about the graph.
        
        Returns:
            Dictionary containing graph statistics
        """
        if self.graph is None:
            return {}
        
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'avg_degree': sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes(),
            'is_directed': self.graph.is_directed(),
            'is_weighted': any('weight' in self.graph[u][v] for u, v in self.graph.edges())
        }
    
    def save_graph(self, filename: str, format: str = 'graphml'):
        """
        Save the graph to a file.
        
        Args:
            filename: Name of the file to save to
            format: Format to save in ('graphml', 'gexf', 'pkl')
        """
        if self.graph is None:
            return
        
        if format == 'graphml':
            ox.save_graphml(self.graph, filename)
        elif format == 'gexf':
            nx.write_gexf(self.graph, filename)
        elif format == 'pkl':
            nx.write_gpickle(self.graph, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def load_graph(self, filename: str, format: str = 'graphml') -> nx.DiGraph:
        """
        Load a graph from a file.
        
        Args:
            filename: Name of the file to load from
            format: Format of the file ('graphml', 'gexf', 'pkl')
            
        Returns:
            NetworkX DiGraph object
        """
        try:
            if format == 'graphml':
                self.graph = ox.load_graphml(filename)
            elif format == 'gexf':
                self.graph = nx.read_gexf(filename)
            elif format == 'pkl':
                self.graph = nx.read_gpickle(filename)
            else:
                raise ValueError(f"Unsupported format: {format}")
            return self.graph
        except Exception as e:
            print(f"Error loading graph from {filename}: {str(e)}")
            return None 