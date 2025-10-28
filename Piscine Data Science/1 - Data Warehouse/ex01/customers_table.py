import os
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
csv_folder_path = "../data/customer"
table_name = "customers"
type_overrides = {
    "event_time": "TIMESTAMP WITH TIME ZONE",
    "user_session": "UUID",
}


def create_table(conn, table_name, csv_folder_path):
    """
    Analyse le premier fichier CSV trouvé pour en déduire le schéma
    et crée la table dans PostgreSQL si elle n'existe pas.
    """
    try:
        file = None
        for filename in os.listdir(csv_folder_path):
            if filename.endswith(".csv"):
                file = os.path.join(csv_folder_path, filename)
                break
        if not file:
            print("No CSV file found in the folder. Table creation aborted.")
            return

        print(f"\nAnalyzing file '{os.path.basename(file)}' for schema...")
        df = pd.read_csv(file, nrows=100)
        type_mapping = {
            "int64": "BIGINT",
            "float64": "DOUBLE PRECISION",
            "bool": "BOOLEAN",
            "datetime64[ns]": "TIMESTAMP",
            "object": "TEXT",
        }

        col_sql = []
        for col_name, col_type in df.dtypes.items():
            col_name_safe = "".join(
                e for e in col_name if e.isalnum() or e == "_"
            )
            if col_name in type_overrides:
                sql_type = type_overrides[col_name]
            else:
                sql_type = type_mapping.get(str(col_type), "TEXT")
            col_sql.append(f'"{col_name_safe}" {sql_type}')

        query = (
            f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(col_sql)});'
        )
        cur = conn.cursor()
        print(f"\nTrying to reach table '{table_name}' (or creating it)...")
        cur.execute(query)
        conn.commit()
        cur.close()
        print(f"Table '{table_name}' ready.\n")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error when creating table: {error}")
        raise


def csv_to_postgres(db_params, csv_folder_path, table_name):
    """
    Charge tous les fichiers CSV d'un dossier dans une table PostgreSQL,
    en créant la table au préalable si elle n'existe pas.
    """
    conn = None
    start_time = time.time()

    try:
        conn = psycopg2.connect(**db_params)
        print("Connected to Postgres Database.")

        create_table(conn, table_name, csv_folder_path)

        cur = conn.cursor()
        for filename in os.listdir(csv_folder_path):
            if filename.startswith("data_202") and filename.endswith(".csv"):
                file_path = os.path.join(csv_folder_path, filename)
                print(f"Loading file: {filename}")
                sql_copy = f"""
                    COPY {table_name} FROM stdin WITH (
                        FORMAT CSV,
                        HEADER,
                        DELIMITER ','
                    )
                """
                with open(file_path, "r", encoding="utf-8") as f:
                    cur.copy_expert(sql=sql_copy, file=f)

        conn.commit()
        print(
            f"\nAll csv files have been copied to table '{table_name}'."
            f" ({time.time() - start_time:.2f}s)"
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print("Disconnected from Postgres Database.")


if __name__ == "__main__":
    csv_to_postgres(db_params, csv_folder_path, table_name)
