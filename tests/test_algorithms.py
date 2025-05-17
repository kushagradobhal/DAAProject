import unittest
import networkx as nx
from src.algorithms import (
    a_star, dijkstra, bellman_ford, floyd_warshall,
    johnson, spfa, bidirectional_dijkstra, yen_k_shortest
)
from src.utils.graph_generator import (
    simple_weighted_graph, negative_weight_graph, disconnected_graph
)

class TestShortestPathAlgorithms(unittest.TestCase):
    def setUp(self):
        """Set up test graphs."""
        self.simple_graph = simple_weighted_graph()
        self.negative_graph = negative_weight_graph()
        self.disconnected_graph = disconnected_graph()
    
    def test_simple_graph(self):
        """Test algorithms on a simple weighted graph."""
        start, end = 'A', 'E'
        expected_path = ['A', 'B', 'C', 'D', 'E']
        expected_cost = 7
        
        # Test each algorithm
        algorithms = [
            (dijkstra.shortest_path, "Dijkstra's"),
            (a_star.shortest_path, "A*"),
            (bellman_ford.shortest_path, "Bellman-Ford"),
            (floyd_warshall.shortest_path, "Floyd-Warshall"),
            (johnson.shortest_path, "Johnson's"),
            (spfa.shortest_path, "SPFA"),
            (bidirectional_dijkstra.shortest_path, "Bidirectional Dijkstra")
        ]
        
        for algorithm, name in algorithms:
            with self.subTest(algorithm=name):
                path, cost = algorithm(self.simple_graph, start, end)
                self.assertEqual(path, expected_path)
                self.assertEqual(cost, expected_cost)
    
    def test_negative_weights(self):
        """Test algorithms on a graph with negative weights."""
        start, end = 'A', 'D'
        expected_path = ['A', 'B', 'C', 'D']
        expected_cost = 3
        
        # Only algorithms that can handle negative weights
        algorithms = [
            (bellman_ford.shortest_path, "Bellman-Ford"),
            (floyd_warshall.shortest_path, "Floyd-Warshall"),
            (johnson.shortest_path, "Johnson's"),
            (spfa.shortest_path, "SPFA")
        ]
        
        for algorithm, name in algorithms:
            with self.subTest(algorithm=name):
                path, cost = algorithm(self.negative_graph, start, end)
                self.assertEqual(path, expected_path)
                self.assertEqual(cost, expected_cost)
    
    def test_disconnected_graph(self):
        """Test algorithms on a disconnected graph."""
        start, end = 'A', 'D'
        
        # All algorithms should return None for disconnected nodes
        algorithms = [
            (dijkstra.shortest_path, "Dijkstra's"),
            (a_star.shortest_path, "A*"),
            (bellman_ford.shortest_path, "Bellman-Ford"),
            (floyd_warshall.shortest_path, "Floyd-Warshall"),
            (johnson.shortest_path, "Johnson's"),
            (spfa.shortest_path, "SPFA"),
            (bidirectional_dijkstra.shortest_path, "Bidirectional Dijkstra")
        ]
        
        for algorithm, name in algorithms:
            with self.subTest(algorithm=name):
                path, cost = algorithm(self.disconnected_graph, start, end)
                self.assertIsNone(path)
                self.assertEqual(cost, float('inf'))
    
    def test_yen_k_shortest(self):
        """Test Yen's K-Shortest Paths algorithm."""
        k = 2
        start, end = 'A', 'E'
        
        paths = yen_k_shortest.shortest_path(self.simple_graph, start, end, k)
        
        # Should return k paths
        self.assertEqual(len(paths), k)
        
        # All paths should be valid
        for path in paths:
            self.assertTrue(nx.is_path(self.simple_graph, path))
        
        # Paths should be in order of increasing cost
        costs = [sum(self.simple_graph[path[i]][path[i+1]]['weight'] 
                    for i in range(len(path)-1)) for path in paths]
        self.assertEqual(costs, sorted(costs))

if __name__ == '__main__':
    unittest.main()
