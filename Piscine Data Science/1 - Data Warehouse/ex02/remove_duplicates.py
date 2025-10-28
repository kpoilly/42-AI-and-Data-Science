from curses import start_color
import sys
import time

import psycopg2


# --- Settings ---
db_params = {
    "host": "localhost",
    "database": "piscineds",
    "user": "kpoilly",
    "password": "mysecretpassword"
}
table_name = 'customers'


def remove_duplicates(db_params, table_name):
    """
    Removes duplicate rows from a PostgreSQL table based on a set of columns.

    :param db_params: A dictionary with database connection parameters.
    :param table_name: The name of the table to clean.
    """

    conn = None
    start_time = time.time()
    deleted_rows_count = 0
    
    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the PostgreSQL database.")

        with conn.cursor() as cur:
            print(f"Fetching column list for table '{table_name}'...")
            info_schema_query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s;
            """
            cur.execute(info_schema_query, (table_name,))
            columns = cur.fetchall()

            if not columns:
                print(f"Error: Could not find table '{table_name}' or it has no columns. Aborting.")
                sys.exit(1)

            column_names = [col[0] for col in columns]
            partition_by_clause = ", ".join(f'"{col}"' for col in column_names)
            query = f"""
            WITH NumberedRows AS (
                SELECT
                    ctid,
                    ROW_NUMBER() OVER (PARTITION BY {partition_by_clause} ORDER BY ctid) as row_num
                FROM
                    {table_name}
            )
            DELETE FROM {table_name}
            WHERE ctid IN (
                SELECT ctid
                FROM NumberedRows
                WHERE row_num > 1
            );
            """
            print(f"Removing duplicates...")
            cur.execute(query)
            deleted_rows_count = cur.rowcount
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
        if conn is not None:
            print("Rolling back the transaction...")
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print("\nDatabase connection closed.")
            print(f"Operation complete. Number of duplicate rows removed: {deleted_rows_count}. ({time.time() - start_time:.2f}s)")
    return deleted_rows_count


if __name__ == '__main__':
    remove_duplicates(db_params, table_name)
