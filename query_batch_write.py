import os
import cx_Oracle
import dask.dataframe as dd
from dask import delayed


def get_total_rows():
    """
    Get the total number of rows in the table.

    Returns:
        int: The total number of rows in the table.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM your_table")
    total_rows = cursor.fetchone()[0]
    return total_rows


@delayed
def fetch_data(offset, batch_size):
    """
    Fetch a chunk of data from the Oracle table and convert it to a Dask DataFrame.

    Parameters:
        offset (int): The starting row number for the data to be fetched.
        batch_size (int): The number of rows to fetch in this batch.

    Returns:
        dask.dataframe.DataFrame: The fetched data as a Dask DataFrame.
    """
    cursor = connection.cursor()
    query = "SELECT * FROM your_table WHERE ROWNUM BETWEEN :start_row AND :end_row"
    cursor.execute(query, start_row=offset, end_row=offset + batch_size - 1)
    
    # Fetch data and convert to Dask DataFrame
    rows = cursor.fetchall()
    df = dd.from_pandas(rows, npartitions=1)
    return df


# Oracle DB connection setup
dsn_tns = cx_Oracle.makedsn('hostname', 'port', service_name='service_name')
connection = cx_Oracle.connect('username', 'password', dsn_tns)


# Initialize a Dask Bag to hold data
dfs = []


# Get total number of rows
total_rows = get_total_rows()


# Define batch size
batch_size = 50000  # Choose a reasonable batch size


# Loop through table and append to Dask Bag
for offset in range(0, total_rows, batch_size):
    dfs.append(fetch_data(offset, batch_size))
    
    # Print progress
    print(f"Fetching rows {offset + 1} to {min(offset + batch_size, total_rows)} out of {total_rows}")


# Concatenate all Dask DataFrames into one
final_ddf = dd.concat(dfs)


# Write Dask DataFrame to CSV
final_ddf.to_csv('output*.csv', index=False).compute()


# Close the Oracle connection
connection.close()