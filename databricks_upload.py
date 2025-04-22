import os
import pandas as pd
from glob import glob
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq

# ---- Configuration ----
local_folder = "/your/local/folder/path/"
source_system = "your_system_name"
volume_target_path = "/Volumes/dev_wmas/bronze/local_files/"
databricks_upload_function = w.files.upload  # Adjust if different

# ---- Step 1: Find Most Recent File (CSV, GZ, XLSX) ----
file_patterns = ["*.csv", "*.csv.gz", "*.xlsx"]
all_files = [f for pattern in file_patterns for f in glob(os.path.join(local_folder, pattern))]

if not all_files:
    raise FileNotFoundError(f"No data files found in {local_folder}")

latest_file = max(all_files, key=os.path.getmtime)
filename = os.path.basename(latest_file)

# ---- Step 2: Read the File into a DataFrame ----
if latest_file.endswith(".csv"):
    df = pd.read_csv(latest_file)
elif latest_file.endswith(".csv.gz"):
    df = pd.read_csv(latest_file, compression='gzip')
elif latest_file.endswith(".xlsx"):
    df = pd.read_excel(latest_file)
else:
    raise ValueError(f"Unsupported file format: {latest_file}")

# ---- Step 3: Add Standard Metadata Columns ----
upload_timestamp = datetime.utcnow().isoformat()
df["upload_date"] = upload_timestamp
df["source_system"] = source_system
df["original_file_name"] = filename

# ---- Step 4: Convert to PyArrow Table with Metadata ----
table = pa.Table.from_pandas(df)

metadata = {
    b"upload_date": upload_timestamp.encode("utf-8"),
    b"source_system": source_system.encode("utf-8"),
    b"original_file_name": filename.encode("utf-8"),
    b"record_count": str(len(df)).encode("utf-8"),
}

table = table.replace_schema_metadata(metadata)

# ---- Step 5: Write to Parquet ----
parquet_filename = os.path.splitext(filename)[0] + ".parquet"
local_parquet_path = os.path.join(local_folder, parquet_filename)

pq.write_table(table, local_parquet_path)

# ---- Step 6: Upload to Databricks Volume ----
target_path = os.path.join(volume_target_path, parquet_filename)
with open(local_parquet_path, "rb") as f:
    databricks_upload_function(target_path, f)

print(f"Uploaded {parquet_filename} to {target_path}")