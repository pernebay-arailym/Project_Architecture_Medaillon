# Validation Great Expectations
#!/usr/bin/env python3
import os
import argparse
import pandas as pd
import great_expectations as gx


def validate_bronze_data(bronze_dir: str):
    """
    Validate Bronze layer Parquet data using Great Expectations.
    """
    print(f" Validating Parquet files in: {bronze_dir}")

    #  Load the datasets
    nodes_path = os.path.join(bronze_dir, "nodes.parquet")
    edges_path = os.path.join(bronze_dir, "edges.parquet")

    nodes_df = pd.read_parquet(nodes_path)
    edges_df = pd.read_parquet(edges_path)

    # Create Great Expectations DataFrames
    gx_nodes = gx.from_pandas(nodes_df)
    gx_edges = gx.from_pandas(edges_df)

    # Define Expectations for nodes
    print(" Checking 'nodes' dataset...")
    gx_nodes.expect_column_values_to_not_be_null("id")
    gx_nodes.expect_column_values_to_be_unique("id")
    gx_nodes.expect_column_values_to_be_in_set("label", ["Person", "Org", "Paper"])

    #  Define Expectations for edges
    print(" Checking 'edges' dataset...")
    gx_edges.expect_column_values_to_not_be_null("src")
    gx_edges.expect_column_values_to_not_be_null("dst")
    gx_edges.expect_column_values_to_be_in_set(
        "type", ["REL", "ASSOCIATED_WITH", "CITED"]
    )

    #  Run validations
    node_result = gx_nodes.validate()
    edge_result = gx_edges.validate()

    # Print summaries
    print("\n Validation Results:")
    print(f"Nodes valid: {node_result.success}")
    print(f"Edges valid: {edge_result.success}")

    #  Optional: save reports to disk
    report_path = os.path.join(bronze_dir, "validation_report.txt")
    with open(report_path, "w") as f:
        f.write("=== Nodes Validation ===\n")
        f.write(str(node_result))
        f.write("\n\n=== Edges Validation ===\n")
        f.write(str(edge_result))

    print(f" Validation report saved to {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Bronze data with Great Expectations."
    )
    parser.add_argument(
        "--in", dest="input_dir", type=str, required=True, help="Bronze data directory"
    )
    args = parser.parse_args()

    validate_bronze_data(args.input_dir)


if __name__ == "__main__":
    main()
