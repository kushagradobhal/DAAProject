import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import sys
import os
import osmnx as ox
from pyvis.network import Network
import streamlit.components.v1 as components

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms import (
    a_star, dijkstra, bellman_ford, floyd_warshall,
    johnson, spfa, bidirectional_dijkstra, yen_k_shortest
)
from src.utils.graph_generator import (
    simple_weighted_graph, negative_weight_graph, disconnected_graph
)
from src.utils.road_network import RoadNetworkLoader
from src.utils.benchmark import AlgorithmBenchmark
from src.utils.graph_utils import select_random_nodes
from src.utils.graph_loader import load_graph_from_csv # Import the CSV loader

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'start_node' not in st.session_state:
    st.session_state.start_node = None
if 'end_node' not in st.session_state:
    st.session_state.end_node = None
if 'road_loader' not in st.session_state:
    st.session_state.road_loader = RoadNetworkLoader()
if 'benchmark_results' not in st.session_state:
    st.session_state.benchmark_results = None
if 'best_path' not in st.session_state:
    st.session_state.best_path = None
if 'best_algo_name' not in st.session_state:
    st.session_state.best_algo_name = None

def create_matplotlib_visualization(graph, path=None):
    """Create a matplotlib visualization of the graph."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # For road networks, use the actual node positions
    if hasattr(graph, 'graph') and 'crs' in graph.graph:
        pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
    else:
        pos = nx.spring_layout(graph)
    
    # Draw nodes with different colors for start, end, and path
    node_colors = []
    node_size = []
    for node in graph.nodes():
        if node == st.session_state.start_node:
            node_colors.append('green') # Start node color
            node_size.append(500) # Larger size for start/end
        elif node == st.session_state.end_node:
            node_colors.append('blue') # End node color
            node_size.append(500) # Larger size for start/end
        elif path and node in path:
            node_colors.append('red') # Path node color
            node_size.append(300)
        else:
            node_colors.append('lightgray') # Other nodes
            node_size.append(300)
            
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_size, ax=ax)
    
    # Draw edges with different colors for the path
    edge_colors = []
    edge_widths = []
    for u, v, data in graph.edges(data=True):
        color = 'gray'
        width = 1.0
        if path:
            # Check if the edge is part of the path in the correct order
            try:
                u_index = path.index(u)
                if u_index < len(path) - 1 and path[u_index + 1] == v:
                    color = 'red' # Path edge color
                    width = 2.0 # Thicker for path edges
            except ValueError:
                pass # u is not in path
        edge_colors.append(color)
        edge_widths.append(width)
    
    # Disable drawing arrows for potentially large or complex graphs to avoid drawing issues
    arrowstyle = '-' # Use a simple line style instead of arrows
    if graph.is_directed():
         nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=edge_widths, arrowstyle=arrowstyle, arrows=False, ax=ax)
    else:
         nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=edge_widths, ax=ax)

    
    # Draw labels for all nodes
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold', ax=ax)
    
    # Draw edge labels if the graph is small enough
    if graph.number_of_edges() < 50:
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        try:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, ax=ax)
        except StopIteration:
            st.warning("Could not draw edge labels due to graph complexity. Please try Pyvis for full visualization.")
    
    return fig

def create_pyvis_visualization(graph, path=None):
    """Create a pyvis visualization of the graph and return HTML content."""
    # Set notebook=True to get HTML content as string
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="#cccccc", notebook=True)
    
    # Add nodes
    for node, data in graph.nodes(data=True):
        color = 'lightgray'
        title = f"Node: {node}"
        size = 20 # Default node size
        
        if node == st.session_state.start_node:
            color = 'green' # Start node color
            title += " (Start)"
            size = 30 # Larger size for start/end
        elif node == st.session_state.end_node:
            color = 'blue' # End node color
            title += " (End)"
            size = 30 # Larger size for start/end
        elif path and node in path:
            color = 'red' # Path node color
            size = 25 # Slightly larger for path nodes
            
        if 'x' in data and 'y' in data:
             title += f"<br>Lat: {data['y']:.4f}<br>Lon: {data['x']:.4f}"
        
        net.add_node(node, label=str(node), color=color, title=title, size=size)

    # Add edges
    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1)
        color = 'gray'
        width = 1 # Default edge width
        title = f"Weight: {weight}"
        
        # Highlight path edges
        if path:
             try:
                 u_index = path.index(u)
                 # Check if directly connected in path sequence and in the correct order
                 if u_index < len(path) - 1 and path[u_index + 1] == v:
                     color = 'red' # Path edge color
                     width = 3 # Thicker for path edges
                     title += " (Shortest Path)"
             except ValueError:
                 pass # u is not in path
        
        net.add_edge(u, v, value=weight, title=title, color=color, width=width)
    
    # Set options for better visualization
    net.set_options("""
    var options = {
      "physics": {
        "enabled": false
      }
    }
    """
)
    
    # Return HTML content as string
    return net.generate_html(notebook=True)

def main():
    st.title("Graph Algorithm Comparator")
    st.write("Compare different shortest path algorithms on various graph types")
    
    # Sidebar for controls
    st.sidebar.header("Controls")
    
    # Graph type selection
    graph_type = st.sidebar.selectbox(
        "Select Graph Type",
        ["Simple Weighted", "Negative Weight", "Disconnected", "Random", "Road Network", "Upload CSV"]
    )
    
    # CSV Upload controls
    if graph_type == "Upload CSV":
        st.sidebar.subheader("Upload CSV Options")
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        directed = st.sidebar.checkbox("Directed Graph", value=False)
        weighted = st.sidebar.checkbox("Weighted Graph", value=True)
        
        if uploaded_file is not None:
            # Save the uploaded file temporarily to a known location
            file_path = os.path.join("temp", uploaded_file.name)
            os.makedirs("temp", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            try:
                st.session_state.graph = load_graph_from_csv(file_path, directed=directed, weighted=weighted)
                st.success(f"Loaded graph from {uploaded_file.name} with {st.session_state.graph.number_of_nodes()} nodes and {st.session_state.graph.number_of_edges()} edges")
                # Select random start and end nodes for the loaded graph
                if st.session_state.graph.number_of_nodes() >= 2:
                     st.session_state.start_node, st.session_state.end_node = select_random_nodes(st.session_state.graph)
                     st.sidebar.write(f"Selected random nodes: {st.session_state.start_node} -> {st.session_state.end_node}")
                else:
                     st.warning("Graph must have at least 2 nodes to select start and end nodes.")
                     st.session_state.start_node = None
                     st.session_state.end_node = None
                     
            except Exception as e:
                 st.error(f"Error loading CSV file: {e}")
                 st.session_state.graph = None


    
    # Road network specific controls
    if graph_type == "Road Network":
        st.sidebar.subheader("Road Network Options")
        place = st.sidebar.text_input("Enter place name (e.g., 'Dehradun, India')")
        network_type = st.sidebar.selectbox(
            "Network Type",
            ["drive", "walk", "bike", "all"]
        )
        
        if st.sidebar.button("Load Road Network"):
            with st.spinner("Loading road network..."):
                st.session_state.graph = st.session_state.road_loader.load_place(place, network_type)
                if st.session_state.graph:
                    st.session_state.graph = st.session_state.road_loader.simplify_graph()
                    st.success(f"Loaded road network with {st.session_state.graph.number_of_nodes()} nodes and {st.session_state.graph.number_of_edges()} edges")
                    
                    # Get graph statistics
                    stats = st.session_state.road_loader.get_graph_stats()
                    st.sidebar.write("Graph Statistics:")
                    for key, value in stats.items():
                        st.sidebar.write(f"{key}: {value}")
    
    # Random Graph Controls
    if graph_type == "Random":
        st.sidebar.subheader("Random Graph Options")
        num_nodes = st.sidebar.slider("Number of nodes", 10, 100, 50)
        edge_prob = st.sidebar.slider("Edge probability", 0.01, 1.0, 0.1, 0.01)
        random_weighted = st.sidebar.checkbox("Weighted", value=True)
        random_directed = st.sidebar.checkbox("Directed", value=False)

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
    
    # Generate graph button for synthetic graphs
    if graph_type != "Road Network" and graph_type != "Upload CSV" and st.sidebar.button("Generate Graph"):
        if graph_type == "Simple Weighted":
            st.session_state.graph = simple_weighted_graph()
        elif graph_type == "Negative Weight":
            st.session_state.graph = negative_weight_graph()
        elif graph_type == "Disconnected":
            st.session_state.graph = disconnected_graph()
        elif graph_type == "Random": # Add the random graph generation here
            st.session_state.graph = nx.erdos_renyi_graph(n=num_nodes, p=edge_prob, directed=random_directed)
            if random_weighted:
                for u, v in st.session_state.graph.edges():
                    st.session_state.graph.edges[u,v]['weight'] = np.random.rand()

        # Select random start and end nodes
        st.session_state.start_node, st.session_state.end_node = select_random_nodes(st.session_state.graph)
        st.sidebar.write(f"Selected random nodes: {st.session_state.start_node} -> {st.session_state.end_node}")
    
    # Node selection for road networks and uploaded CSVs (if graph loaded)
    if (graph_type == "Road Network" or graph_type == "Upload CSV") and st.session_state.graph:
        st.sidebar.subheader("Node Selection")
        
        # If it's a road network, provide specific node selection options
        if graph_type == "Road Network":
             node_selection = st.sidebar.radio(
                 "Select nodes by",
                 ["Random", "Farthest Apart"]
             )
             if st.sidebar.button("Select Nodes"):
                 if node_selection == "Random":
                     pairs = st.session_state.road_loader.get_random_nodes(1)
                 else:
                     pairs = st.session_state.road_loader.get_farthest_nodes(1)
                 
                 if pairs:
                     st.session_state.start_node, st.session_state.end_node = pairs[0]
                     st.success(f"Selected nodes: {st.session_state.start_node} -> {st.session_state.end_node}")
        
        # If it's a loaded CSV, allow manual node selection
        elif graph_type == "Upload CSV":
             nodes = list(st.session_state.graph.nodes())
             # Ensure selected nodes are in the graph, default to first/last if not
             default_start_index = nodes.index(st.session_state.start_node) if st.session_state.start_node in nodes else (0 if nodes else None)
             default_end_index = nodes.index(st.session_state.end_node) if st.session_state.end_node in nodes else (len(nodes)-1 if nodes else None)
             
             st.session_state.start_node = st.sidebar.selectbox("Select Start Node", nodes, index=default_start_index)
             st.session_state.end_node = st.sidebar.selectbox("Select End Node", nodes, index=default_end_index)

    
    # Visualization type selection
    visualization_type = st.sidebar.radio(
        "Select Visualization Type",
        ["Matplotlib", "Pyvis"]
    )
    
    # Main content area
    if st.session_state.graph is not None:
        # Display graph
        st.subheader("Graph Visualization")
        
        if visualization_type == "Matplotlib":
            fig = create_matplotlib_visualization(st.session_state.graph, st.session_state.best_path)
            # Only display the figure if create_matplotlib_visualization returned one
            if fig is not None:
                st.pyplot(fig)
        elif visualization_type == "Pyvis":
            # Pyvis needs node positions for road networks, but can use default for others
            if graph_type != "Road Network" and graph_type != "Upload CSV":
                 # Add a default layout for Pyvis if not road network or CSV
                 for node in st.session_state.graph.nodes():
                     if 'x' not in st.session_state.graph.nodes[node] or 'y' not in st.session_state.graph.nodes[node]:
                          st.session_state.graph.nodes[node]['x'] = np.random.rand()
                          st.session_state.graph.nodes[node]['y'] = np.random.rand()
                     
            # Get HTML content as string
            html_content = create_pyvis_visualization(st.session_state.graph, st.session_state.best_path)
            
            # Display the HTML in the Streamlit app
            components.html(html_content, height=800, scrolling=True)
            
        
        # Run algorithms
        if st.button("Run Selected Algorithms"):
            if st.session_state.start_node is None or st.session_state.end_node is None:
                 st.warning("Please select start and end nodes first.")
            else:
                benchmark = AlgorithmBenchmark()
                selected_algo_dict = {name: algorithms[name] for name in selected_algorithms}
                results = benchmark.run_benchmark(
                    selected_algo_dict,
                    st.session_state.graph,
                    st.session_state.start_node,
                    st.session_state.end_node
                )
                
                # Store benchmark results and best path in session state
                st.session_state.benchmark_results = results
                
                # Display results
                st.subheader("Results")
                
                # Performance metrics
                st.write("Performance Metrics")
                # Include the 'success' column to show if a path was found
                st.dataframe(st.session_state.benchmark_results[['algorithm', 'execution_time', 'memory_used_mb', 'path_length', 'path_cost', 'success']])
                
                # Visualize best path
                best_algo = st.session_state.benchmark_results.loc[st.session_state.benchmark_results['path_cost'].idxmin()]
                
                # Check if a path was actually found for the best algorithm
                if best_algo['success']:
                    st.session_state.best_algo_name = best_algo['algorithm']
                    st.subheader(f"Best Path (using {st.session_state.best_algo_name})")
                    # Re-run the best algorithm to get the path for visualization
                    st.session_state.best_path, _ = algorithms[st.session_state.best_algo_name](
                        st.session_state.graph,
                        st.session_state.start_node,
                        st.session_state.end_node
                    )
                    
                    # Re-render the graph visualization with the stored best_path
                    if visualization_type == "Matplotlib":
                         fig = create_matplotlib_visualization(st.session_state.graph, st.session_state.best_path)
                         # Only display the figure if create_matplotlib_visualization returned one
                         if fig is not None:
                             st.pyplot(fig)
                    elif visualization_type == "Pyvis":
                         # For Pyvis, we need to regenerate the visualization with the path highlighted
                         # Pyvis needs node positions for road networks, but can use default for others
                         if graph_type != "Road Network" and graph_type != "Upload CSV":
                              # Add a default layout for Pyvis if not road network or CSV
                              for node in st.session_state.graph.nodes():
                                   if 'x' not in st.session_state.graph.nodes[node] or 'y' not in st.session_state.graph.nodes[node]:
                                       st.session_state.graph.nodes[node]['x'] = np.random.rand()
                                       st.session_state.graph.nodes[node]['y'] = np.random.rand()
                                  
                         # Get HTML content as string
                         html_content = create_pyvis_visualization(st.session_state.graph, st.session_state.best_path)
                         components.html(html_content, height=800, scrolling=True)
                else:
                    # Display a message if the best algorithm didn't find a path
                    st.warning(f"No path found by {best_algo['algorithm']} between selected nodes.")
                    st.session_state.best_path = None # Clear the best path if none found
                    st.session_state.best_algo_name = None # Clear the best algo name

            
            # Save results
            if st.button("Save Results"):
                # Ensure there are results to save
                if st.session_state.benchmark_results is not None:
                    benchmark.save_results("benchmark_results.csv")
                    st.success("Results saved to benchmark_results.csv")
                else:
                    st.info("No results to save yet. Run algorithms first.")

    # Display benchmark results and best path info if available in session state (after rerun)
    # This section is mainly to persist display after a rerun triggered by node selection etc.
    if st.session_state.benchmark_results is not None:
         st.subheader("Results")
         st.write("Performance Metrics")
         # Include the 'success' column here as well
         st.dataframe(st.session_state.benchmark_results[['algorithm', 'execution_time', 'memory_used_mb', 'path_length', 'path_cost', 'success']])
         
         if st.session_state.best_algo_name and st.session_state.best_path:
              st.subheader(f"Best Path (using {st.session_state.best_algo_name})")
              # The graph visualization will be re-rendered above with the stored best_path

if __name__ == "__main__":
    main() 