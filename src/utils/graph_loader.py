import networkx as nx
import pandas as pd

def load_graph_from_csv(file_path, directed=False, weighted=True):
    df = pd.read_csv(file_path)
    G = nx.DiGraph() if directed else nx.Graph()

    for _, row in df.iterrows():
        u, v = int(row['source']), int(row['target'])
        w = float(row['weight']) if weighted and 'weight' in row else 1
        G.add_edge(u, v, weight=w)

    return G
