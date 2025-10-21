# Génération de données
import os
import argparse
import numpy as np
import pandas as pd


def generate_nodes(num_nodes: int) -> pd.DataFrame:
    """Generate synthetic node data."""
    labels = np.random.choice(["Person", "Org", "Paper"], size=num_nodes)
    names = [f"name_{i}" for i in range(num_nodes)]
    df_nodes = pd.DataFrame(
        {"id": np.arange(num_nodes), "label": labels, "name": names}
    )
    return df_nodes


def generate_edges(num_edges: int, num_nodes: int) -> pd.DataFrame:
    """Generate synthetic edge data."""
    src = np.random.randint(0, num_nodes, size=num_edges)
    dst = np.random.randint(0, num_nodes, size=num_edges)
    rel_types = np.random.choice(["REL", "ASSOCIATED_WITH", "CITED"], size=num_edges)
    df_edges = pd.DataFrame({"src": src, "dst": dst, "type": rel_types})
    return df_edges


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic Knowledge Graph data."
    )
    parser.add_argument("--out", type=str, default="data/raw", help="Output directory")
    parser.add_argument(
        "--nodes", type=int, default=10000, help="Number of nodes to generate"
    )
    parser.add_argument(
        "--edges", type=int, default=50000, help="Number of edges to generate"
    )
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    print(f"Generating {args.nodes} nodes and {args.edges} edges...")
    nodes = generate_nodes(args.nodes)
    edges = generate_edges(args.edges, args.nodes)

    nodes_path = os.path.join(args.out, "nodes.csv")
    edges_path = os.path.join(args.out, "edges.csv")

    nodes.to_csv(nodes_path, index=False)
    edges.to_csv(edges_path, index=False)

    print(f" Data generated:")
    print(f"  Nodes → {nodes_path}")
    print(f"  Edges → {edges_path}")


if __name__ == "__main__":
    main()
