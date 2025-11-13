#!/usr/bin/env python3
import os
import argparse
import pandas as pd
import numpy as np


def partition_edges(input_dir: str, output_dir: str, partitions: int):
    # Partition edges into N shards and copy nodes as-is.

    os.makedirs(output_dir, exist_ok=True)

    # Load data
    edges = pd.read_parquet(os.path.join(input_dir, "edges.parquet"))
    nodes = pd.read_parquet(os.path.join(input_dir, "nodes.parquet"))

    # Assign a shard number randomly to each edge
    edges["shard"] = np.random.randint(0, partitions, size=len(edges))

    # Write each shard
    for shard in range(partitions):
        shard_dir = os.path.join(output_dir, f"shard={shard}")
        os.makedirs(shard_dir, exist_ok=True)
        shard_df = edges[edges["shard"] == shard].drop(columns=["shard"])
        shard_df.to_parquet(os.path.join(shard_dir, "edges.parquet"), index=False)
        print(f"Wrote shard {shard} with {len(shard_df)} edges")

    # Copy nodes as-is (only one file)
    nodes.to_parquet(os.path.join(output_dir, "nodes.parquet"), index=False)
    print(f"Copied nodes file to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Partition edges into shards for Silver layer."
    )
    parser.add_argument(
        "--in", dest="input_dir", type=str, required=True, help="Input Bronze directory"
    )
    parser.add_argument(
        "--out",
        dest="output_dir",
        type=str,
        required=True,
        help="Output Silver directory",
    )
    parser.add_argument(
        "--partitions", type=int, default=8, help="Number of shards to create"
    )
    args = parser.parse_args()

    partition_edges(args.input_dir, args.output_dir, args.partitions)


if __name__ == "__main__":
    main()
