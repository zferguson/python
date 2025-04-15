# pip install databricks-cli
# databricks configure --profile <your-profile>

import os
import subprocess

def upload_to_dbfs(local_path: str, dbfs_path: str):
    """
    Uploads a local file to DBFS using Databricks CLI.
    Assumes you have configured `databricks configure` with a profile.
    """
    # Upload file using databricks CLI
    try:
        result = subprocess.run(
            ["databricks", "fs", "cp", "--overwrite", local_path, dbfs_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("Upload successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error uploading file:", e.stderr)

# Example usage
upload_to_dbfs("data/myfile.csv", "dbfs:/mnt/myvolume/myfile.csv")