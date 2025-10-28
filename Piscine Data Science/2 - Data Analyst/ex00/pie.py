import sys

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# --- Settings ---
db_params = {
    "host": "localhost",
    "database": "piscineds",
    "user": "kpoilly",
    "password": "mysecretpassword",
}
table_name = "customers"


def analyze_user_events(db_params, table_name):
    """
    Se connecte à la base de données, analyse la répartition des types d'événements
    et génère un diagramme circulaire.
    """
    conn = None
    print("Starting user event analysis...")

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")

        query = f"""
            SELECT
                event_type,
                COUNT(*) AS event_count
            FROM
                {table_name}
            GROUP BY
                event_type
            ORDER BY
                event_count DESC;
        """

        print("Fetching data...")
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("The table is empty.")
            return

        print("\n--- Summary of User Events ---")
        print(df.to_string(index=False))

        print("\nGenerating pie chart...")
        event_types = df["event_type"]
        event_counts = df["event_count"]
        explode = [0] * len(event_types)
        explode[0] = 0.1

        plt.figure(figsize=(12, 8))
        plt.pie(
            event_counts,
            labels=event_types,
            autopct="%1.1f%%",
            startangle=140,
            explode=explode,
            shadow=True,
        )
        plt.title("Distribution of User Events on the Site", fontsize=16)
        plt.axis("equal")
        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nAN ERROR OCCURRED: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    analyze_user_events(db_params, table_name)
