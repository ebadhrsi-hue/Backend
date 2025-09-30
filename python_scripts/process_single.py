import sys
import pandas as pd
from sqlalchemy import create_engine


def merge_sql_excel(
    server, database, username, password,
    table_name, excel_path,
    save_to_sql=False, save_to_excel=False, excel_out_path="merged_output.xlsx"
):
    """
    Merge SQL Server table (df_a) with Excel file (df_b) using Candidate_ID.
    If Candidate_ID matches, replace df_a row with df_b row.
    If Candidate_ID only exists in df_b, append it.
    
    Parameters:
        server (str): SQL Server hostname
        database (str): Database name
        username (str): SQL Server username
        password (str): SQL Server password
        table_name (str): Table name in SQL Server
        excel_path (str): Path to Excel file
        save_to_sql (bool): If True, overwrite table in SQL Server
        save_to_excel (bool): If True, save merged DataFrame to Excel
        excel_out_path (str): Path for output Excel file
    
    Returns:
        df_final (DataFrame): Final merged DataFrame
    """
    
    # --- Step 1: Connect to SQL Server ---
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(connection_string, fast_executemany=True)

    # --- Step 2: Load SQL table and Excel file ---
    df_a = pd.read_sql(f"SELECT * FROM [{table_name}]", engine)
    df_b = pd.read_excel(excel_path)

    # --- Step 3: Ensure Candidate_ID column is consistent type ---
    df_a['Candidate_ID'] = df_a['Candidate_ID'].astype(str).str.strip()
    # Excel might have column named "Candidate ID" with space
    if 'Candidate ID' in df_b.columns:
        df_b.rename(columns={'Candidate ID': 'Candidate_ID'}, inplace=True)
    df_b['Candidate_ID'] = df_b['Candidate_ID'].astype(str).str.strip()

    # --- Step 4: Drop matching Candidate_IDs from df_a ---
    mask = df_a['Candidate_ID'].isin(df_b['Candidate_ID'])
    df_a_filtered = df_a[~mask]   # Keep only rows not in df_b

    # --- Step 5: Append df_b (replace matches + add new ones) ---
    df_final = pd.concat([df_a_filtered, df_b], ignore_index=True)

    # --- Step 6: Optional save ---
    if save_to_sql:
        df_final.to_sql(table_name, engine, if_exists="replace", index=False)
    if save_to_excel:
        df_final.to_excel(excel_out_path, index=False)

    return df_final

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process_single.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Load your df_a from SQL Server (already done)
        df_a = merge_sql_excel(
    server="rdmc.database.windows.net",
    database="rdmc",
    username="ebad",
    password='Iba"2395',
    table_name="MasterData-Current",
    excel_path=input_file,
    save_to_sql=False,   # set True if you want to overwrite SQL table
    save_to_excel=False,  # set True if you want Excel output
    excel_out_path="merged_output.xlsx"
)

        # Optional: do something with input_file if needed
        # e.g., read input_file and merge with df_a, or ignore it

        # Save df_a as Excel to output_file
        df_a.to_excel(output_file, index=False)

        print("File processed and saved successfully")
    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)
