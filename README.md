# 🏗️ Knowledge Graph Pipeline — Medallion Architecture (Bronze → Silver)

A complete **Data Engineering pipeline** built using the **Medallion Architecture** (Bronze → Silver → Gold).  
This repository demonstrates how to generate synthetic Knowledge Graph data, process it through structured ETL layers, validate data quality, and prepare it for graph database ingestion.

This project is built focusing on real architecture patterns using **Python, Parquet, Great Expectations, Airflow, and Neo4j**.

---

## 📐 Architecture Overview

             ┌──────────────────────┐
             │   Synthetic Data      │
             │  (Nodes + Edges CSV)  │
             └───────────┬──────────┘
                         ▼
            🥉 BRONZE LAYER (Raw → Parquet)
          - Convert CSV → Parquet
          - Store raw structured data

                         ▼
            🥈 SILVER LAYER (Validated + Partitioned)
          - Data validation with Great Expectations
          - Partition edges into shards (for scalability)

                         ▼
            🥇 GOLD LAYER (Preparation for Neo4j)
          - (Next step) CSV formatting
          - (Next step) Neo4j bulk import

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3** | ETL scripting (data generation, conversion, validation) |
| **NumPy / Pandas** | Data manipulation |
| **Parquet** | Optimized columnar storage |
| **Great Expectations** | Data quality validation |
| **Docker** | Running Airflow + Neo4j |
| **Neo4j** | Graph database (Gold layer target) |
| **Airflow** | Pipeline orchestration |
| **Makefile** | Developer automation |

---

## 🚀 Features Implemented So Far

### Phase 1 — Project Architecture  
- Structured Medallion-based project layout  
- Dockerized Airflow + Neo4j  
- Makefile with automation commands  

---

### Phase 2 — Synthetic Data Generation (`generate_sample_data.py`)  

Generates two CSV files:  
- **nodes.csv** → id, label, name  
- **edges.csv** → src, dst, type  

You can define the number of nodes + edges:

```
python3 scripts/generate_sample_data.py --nodes 10000 --edges 50000 --out data/raw
```

---

### Phase 3 — Bronze Layer (CSV → Parquet)

Script: scripts/to_parquet.py

Converts raw CSV files into Parquet format:

```
python3 scripts/to_parquet.py --in data/raw --out data/bronze
```

---

### Phase 4 — Silver Layer: Data Quality + Partitioning
🔍 Data Validation (Great Expectations)

Script: ```quality/gx_checkpoint.py```

Checks:

- No nulls in critical fields
- Unique IDs
- Label/type values from allowed sets
- Valid structure for relationships

Run:
```
python3 quality/gx_checkpoint.py --in data/bronze
```

Uses Great Expectations functions like:
```
expect_column_values_to_not_be_null()
expect_column_values_to_be_unique()
expect_column_values_to_be_in_set()
```

A validation report is saved in:
```data/bronze/validation_report.txt```

### 🧩 Edge Partitioning (Sharding)

Script: ```scripts/partition_edges.py```

Run:
```
python3 scripts/partition_edges.py --in data/bronze --out data/silver --partitions 8
```

---

### 📦 Makefile Automation
```
seed:
	python3 scripts/generate_sample_data.py --out data/raw --nodes 10000 --edges 50000

bronze:
	python3 scripts/to_parquet.py --in data/raw --out data/bronze

check_quality:
	python3 quality/gx_checkpoint.py --in data/bronze

silver:
	python3 scripts/partition_edges.py --in data/bronze --out data/silver --partitions 8

# Preparing for next step:
gold:
	bash scripts/neo4j_bulk_import.sh

e2e:
	make seed
	make bronze
	make check_quality
	make silver
```

Run everything:
```
make e2e
```
---

### 📚 Great Expectations Summary

Here are the main GX expectations used:

| Expectation                             | Purpose                                  |
| --------------------------------------- | ---------------------------------------- |
| `expect_column_values_to_not_be_null()` | Ensure required fields exist             |
| `expect_column_values_to_be_unique()`   | Validate ID uniqueness                   |
| `expect_column_values_to_be_in_set()`   | Validate semantic correctness            |
| `.validate()`                           | Run all expectations and return a result |


Validation produces:
- Terminal output
- Text report in the Bronze folder

---

### 🧭 Next Steps (Gold Layer)

- Convert Silver Parquet → Neo4j-compatible CSV
- Use neo4j-admin import for bulk ingestion
- Trigger everything via Airflow DAG
