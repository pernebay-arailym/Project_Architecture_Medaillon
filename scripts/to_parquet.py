# Conversion CSV→Parquet

import os
import argparse
import pandas as pd


def convert_csv_to_parquet(input_dir: str, output_dir: str):
    #Convert CSV files in input_dir to Parquet files in output_dir.
    
    os.makedirs(output_dir, exist_ok=True)

    # Define file paths
    files = {
        "nodes": os.path.join(
            input_dir,
            "nodes.csv",
        ),
        "edges": os.path.join(
            input_dir,
            "edges.csv",
        ),
    }

    for name, path in files.items():
        if not os.path.exists(path):
            print(f" File not found: {path}")
            continue

        print(f" Reading {name} from {path}")
        df = pd.read_csv(path)

        # Save to parquet (auto-compression)
        out_path = os.path.join(output_dir, f"{name}.parquet")
        df.to_parquet(out_path, index=False)
        print(f" Saved {name} to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert CSV files to Parquet format.")
    parser.add_argument(
        "--in",
        dest="input_dir",
        type=str,
        required=True,
        help="Input directory containing CSV files",
    )
    parser.add_argument(
        "--out",
        dest="output_dir",
        type=str,
        required=True,
        help="Output directory for Parquet files",
    )
    args = parser.parse_args()

    convert_csv_to_parquet(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
