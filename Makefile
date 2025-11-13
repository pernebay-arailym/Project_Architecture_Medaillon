#commandes pratiaues

seed:
	python3 scripts/generate_sample_data.py --out data/raw --nodes 100000 --edges 500000

bronze:
	python3 scripts/to_parquet.py --in data/raw --out data/bronze

check_quality:
	python3 quality/gx_checkpoint.py --in data/bronze
