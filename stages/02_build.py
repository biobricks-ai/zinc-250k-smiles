import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import sys

input_dir = Path("download")
output_dir = Path("brick")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "data.parquet"

# Find the csv file
csv_files = list(input_dir.glob("*.csv"))
if not csv_files:
    print("No CSV files found in download directory.")
    sys.exit(1)

input_file = csv_files[0]
print(f"Processing {input_file}...")

# Load data
df = pd.read_csv(input_file)

# Standardize columns
# ZINC250k usually has 'smiles', 'logP', 'qed', 'SAS'
df.columns = [c.lower().strip() for c in df.columns]

if 'smiles' not in df.columns:
    print(f"Columns found: {df.columns}")
    # Fallback: check if the first column looks like smiles
    # But usually this dataset is well formed.
    raise ValueError("Could not find 'smiles' column.")

# Ensure SMILES is a string
df['smiles'] = df['smiles'].astype(str)

# Convert numeric columns if they exist
numeric_cols = ['logp', 'qed', 'sas']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Write to parquet
table = pa.Table.from_pandas(df)
pq.write_table(table, output_file)
print(f"Written {len(df)} records to {output_file}")
