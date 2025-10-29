import sys

import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- Settings ---
db_params = {
    "host": "localhost",
    "database": "piscineds",
    "user": "kpoilly",
    "password": "mysecretpassword",
}
table_name = "customers"


def find_optimal_clusters(db_params, table_name):
    """
    Récupère les données de Fréquence et Valeur Monétaire, puis utilise
    la méthode du coude pour trouver le nombre optimal de clusters de clients.
    """
    conn = None
    print("Starting Elbow Method for customer clustering...")

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")

        query_rfm = f"""
            SELECT
                user_id,
                COUNT(DISTINCT user_session) AS frequency,
                SUM(price) AS monetary_value
            FROM {table_name}
            WHERE event_type = 'purchase'
            GROUP BY user_id
            HAVING SUM(price) > 0;
        """
        print("Fetching and calculating RFM data per user...")
        df_rfm = pd.read_sql_query(query_rfm, conn)
        if df_rfm.empty:
            print("No data found to perform clustering.")
            return

        X = df_rfm[["frequency", "monetary_value"]]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        print("Calculating inertia for a range of clusters (1 to 10)...")
        wcss = []
        for k in range(1, 11):
            kmeans = KMeans(
                n_clusters=k,
                init="k-means++",
                n_init=10,
                max_iter=300,
                random_state=42,
            )
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)

        print("Generating the Elbow Method plot...")
        sns.set_style("darkgrid")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=range(1, 11), y=wcss, marker="o")
        plt.title("The Elbow Method")
        plt.xlabel("Number of clusters")
        plt.ylabel("")
        plt.xticks(range(1, 11))

        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    find_optimal_clusters(db_params, table_name)
