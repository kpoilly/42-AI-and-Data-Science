import os
import sys
import time

import psycopg2
import pandas as pd

# --- Settings ---
db_params = {
    "host": "localhost",
    "database": "piscineds",
    "user": "kpoilly",
    "password": "mysecretpassword",
}
main_table = "customers"
new_csv_folder_path = "../data/item"
join_key = "product_id"


def enrich_main_table(db_params, main_table, join_key, csv_path):
    """
    Enriches a main table with data from new CSV files using a staging table.

    :param db_params: Database connection details.
    :param main_table: The target table to enrich (e.g., 'customers').
    :param join_key: The column name to use for the JOIN operation.
    :param csv_path: The folder path containing the new CSV files.
    """
    conn = None
    start_time = time.time()
    staging_table = "staging_items"
    new_table = f"{main_table}_new"

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to Postgres database.")

        with conn.cursor() as cur:
            print(f"\nImporting data to staging table '{staging_table}'...")
            first_csv = next(
                (
                    os.path.join(csv_path, f)
                    for f in os.listdir(csv_path)
                    if f.endswith(".csv")
                ),
                None,
            )
            if not first_csv:
                print(
                    f"Error: No CSV files found in '{csv_path}'. Aborting.",
                    file=sys.stderr,
                )
                return

            df = pd.read_csv(first_csv, nrows=100)
            type_mapping = {
                "int64": "BIGINT",
                "float64": "DOUBLE PRECISION",
                "object": "TEXT",
            }
            sql_columns = [
                f'"{col}" {type_mapping.get(str(df.dtypes[col]), "TEXT")}'
                for col in df.columns
            ]
            cur.execute(f"DROP TABLE IF EXISTS {staging_table};")
            cur.execute(
                f"CREATE TABLE {staging_table} ({', '.join(sql_columns)});"
            )

            for filename in os.listdir(csv_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(csv_path, filename)
                    print(f"Loading file: {filename}")
                    sql_copy = f"""
                    COPY {staging_table} FROM stdin WITH (
                        FORMAT CSV,
                        HEADER,
                        DELIMITER ','
                    )
                """
                    with open(file_path, "r", encoding="utf-8") as f:
                        cur.copy_expert(sql=sql_copy, file=f)

            print(f"\nCreating new table '{new_table}'...")
            staging_columns = [
                f's."{col}"' for col in df.columns if col != join_key
            ]
            create_query = f"""
            CREATE TABLE {new_table} AS
            SELECT
                m.*,
                {', '.join(staging_columns)}
            FROM
                {main_table} AS m
            LEFT JOIN
                {staging_table} AS s ON m."{join_key}" = s."{join_key}";
            """
            cur.execute(create_query)
            print(f"new table '{new_table}' created successfully.")

            print("\nSwapping old table with the new one...")
            cur.execute(f"DROP TABLE {main_table};")
            cur.execute(f"ALTER TABLE {new_table} RENAME TO {main_table};")
            print("Table swap complete.")

            print("\nCleaning temp table...")
            cur.execute(f"DROP TABLE {staging_table};")
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nAN ERROR OCCURRED: {error}", file=sys.stderr)
        if conn is not None:
            print("Rolling back transaction...")
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print("\nDatabase connection closed.")
        print(f"Enrichment process finished. ({time.time()-start_time:.2f}s)")


if __name__ == "__main__":
    enrich_main_table(db_params, main_table, join_key, new_csv_folder_path)
