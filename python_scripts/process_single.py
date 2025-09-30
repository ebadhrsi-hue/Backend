import sys
import shutil

import pandas as pd
from sqlalchemy import create_engine

# --- Step 1: Connect to SQL Server and load table into df_a ---
server = 'rdmc.database.windows.net'
database = 'rdmc'
username = 'ebad'
password = 'Iba"2395'

# Using SQLAlchemy with pyodbc
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string,fast_executemany=True)

# Read table into DataFrame
df_a = pd.read_sql("SELECT * FROM [MasterData-Current]", engine)





if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process_single.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Just copy the file back unchanged
        shutil.copyfile(input_file, output_file)
        print("File returned successfully:", output_file)
    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)
