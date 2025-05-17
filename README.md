# Graph Algorithm Comparator

A comprehensive tool for comparing, analyzing, and visualizing multiple shortest path algorithms on various graph types.

## Features

- **Multiple Algorithm Support**:
  - Dijkstra's Algorithm
  - A* Search
  - Bellman-Ford Algorithm
  - Floyd-Warshall Algorithm
  - Johnson's Algorithm
  - SPFA (Shortest Path Faster Algorithm)
  - Bidirectional Dijkstra
  - Yen's K-Shortest Paths

- **Graph Types**:
  - Simple weighted graphs
  - Graphs with negative weights
  - Disconnected graphs
  - Random graphs

- **Visualization**:
  - Interactive graph visualization
  - Path highlighting
  - Performance metrics display
  - Side-by-side algorithm comparison

- **Performance Analysis**:
  - Execution time measurement
  - Memory usage tracking
  - Path cost comparison
  - Results export to CSV

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/graph-algorithm-comparator.git
cd graph-algorithm-comparator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/app.py
```

2. In the web interface:
   - Select the graph type
   - Choose algorithms to compare
   - Generate a graph
   - Run the comparison
   - View results and visualizations

## Project Structure

```
graph-algorithm-comparator/
├── src/
│   ├── algorithms/
│   │   ├── a_star.py
│   │   ├── bellman_ford.py
│   │   ├── dijkstra.py
│   │   └── ...
│   ├── utils/
│   │   ├── benchmark.py
│   │   ├── graph_generator.py
│   │   └── ...
│   └── app.py
├── tests/
│   └── test_algorithms.py
├── requirements.txt
└── README.md
```

## Running Tests

```bash
python -m unittest tests/test_algorithms.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NetworkX for graph operations
- Streamlit for the web interface
- Matplotlib for visualization
