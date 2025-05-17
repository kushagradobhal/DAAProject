import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, Any
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import (
    a_star, dijkstra, bellman_ford, floyd_warshall,
    johnson, spfa, bidirectional_dijkstra, yen_k_shortest
)
from src.utils.graph_generator import (
    simple_weighted_graph, negative_weight_graph, disconnected_graph
)
from src.utils.benchmark import AlgorithmBenchmark
from src.utils.graph_utils import select_random_nodes

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'start_node' not in st.session_state:
    st.session_state.start_node = None
if 'end_node' not in st.session_state:
    st.session_state.end_node = None

def create_graph_visualization(graph, path=None):
    """Create a matplotlib visualization of the graph."""
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    
    # Draw nodes
    node_colors = []
    for node in graph.nodes():
        if path and node in path:
            node_colors.append('red')
        elif node == st.session_state.start_node:
            node_colors.append('green')
        elif node == st.session_state.end_node:
            node_colors.append('blue')
        else:
            node_colors.append('lightgray')
    
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors)
    nx.draw_networkx_labels(graph, pos)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    return plt

def main():
    st.title("Graph Algorithm Comparator")
    st.write("Compare different shortest path algorithms on various graph types")
    
    # Sidebar for controls
    st.sidebar.header("Controls")
    
    # Graph type selection
    graph_type = st.sidebar.selectbox(
        "Select Graph Type",
        ["Simple Weighted", "Negative Weight", "Disconnected", "Random"]
    )
    
    # Algorithm selection
    algorithms = {
        "Dijkstra's": dijkstra.shortest_path,
        "A*": a_star.shortest_path,
        "Bellman-Ford": bellman_ford.shortest_path,
        "Floyd-Warshall": floyd_warshall.shortest_path,
        "Johnson's": johnson.shortest_path,
        "SPFA": spfa.shortest_path,
        "Bidirectional Dijkstra": bidirectional_dijkstra.shortest_path,
        "Yen's K-Shortest": yen_k_shortest.shortest_path
    }
    
    selected_algorithms = st.sidebar.multiselect(
        "Select Algorithms to Compare",
        list(algorithms.keys()),
        default=["Dijkstra's", "A*"]
    )
    
    # Generate graph button
    if st.sidebar.button("Generate Graph"):
        if graph_type == "Simple Weighted":
            st.session_state.graph = simple_weighted_graph()
        elif graph_type == "Negative Weight":
            st.session_state.graph = negative_weight_graph()
        elif graph_type == "Disconnected":
            st.session_state.graph = disconnected_graph()
        else:
            # Random graph generation logic here
            pass
        
        # Select random start and end nodes
        st.session_state.start_node, st.session_state.end_node = select_random_nodes(st.session_state.graph)
    
    # Main content area
    if st.session_state.graph is not None:
        # Display graph
        st.subheader("Graph Visualization")
        fig = create_graph_visualization(st.session_state.graph)
        st.pyplot(fig)
        
        # Run algorithms
        if st.button("Run Selected Algorithms"):
            benchmark = AlgorithmBenchmark()
            selected_algo_dict = {name: algorithms[name] for name in selected_algorithms}
            results = benchmark.run_benchmark(
                selected_algo_dict,
                st.session_state.graph,
                st.session_state.start_node,
                st.session_state.end_node
            )
            
            # Display results
            st.subheader("Results")
            
            # Performance metrics
            st.write("Performance Metrics")
            st.dataframe(results[['algorithm', 'execution_time', 'memory_used_mb', 'path_length', 'path_cost']])
            
            # Visualize best path
            best_algo = results.loc[results['path_cost'].idxmin()]
            if best_algo['success']:
                st.subheader(f"Best Path (using {best_algo['algorithm']})")
                best_path = algorithms[best_algo['algorithm']](
                    st.session_state.graph,
                    st.session_state.start_node,
                    st.session_state.end_node
                )[0]
                fig = create_graph_visualization(st.session_state.graph, best_path)
                st.pyplot(fig)
            
            # Save results
            if st.button("Save Results"):
                benchmark.save_results("benchmark_results.csv")
                st.success("Results saved to benchmark_results.csv")

if __name__ == "__main__":
    main() 