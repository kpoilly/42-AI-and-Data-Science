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
N_CLUSTERS = 4


def create_customer_segments(db_params, table_name):
    """
    Crée des segments de clients en utilisant K-Means
    basé sur les métriques de Récence, Fréquence et Valeur Monétaire.
    """
    conn = None
    print("Starting customer segmentation process...")

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")

        query_max_date = f"SELECT MAX(event_time) FROM {table_name};"
        max_date = pd.read_sql_query(query_max_date, conn).iloc[0, 0]

        query_rfm = f"""
            SELECT
                user_id,
                DATE_PART(
                    'day', '{max_date}'::TIMESTAMP - MAX(event_time)
                ) AS recency,
                COUNT(DISTINCT user_session) AS frequency,
                SUM(price) AS monetary_value
            FROM {table_name}
            WHERE event_type = 'purchase'
            GROUP BY user_id
            HAVING SUM(price) > 0;
        """
        df_rfm = pd.read_sql_query(query_rfm, conn, index_col="user_id")
        if df_rfm.empty:
            print("No data found for segmentation.")
            return

        print(f"Applying K-Means to create {N_CLUSTERS} segments...")

        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(df_rfm)
        kmeans = KMeans(
            n_clusters=N_CLUSTERS,
            init="k-means++",
            n_init=10,
            max_iter=300,
            random_state=42,
        )
        df_rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

        print("Analyzing cluster characteristics...")
        rfm_summary = df_rfm.groupby("cluster").agg(
            recency=("recency", "median"),
            frequency=("frequency", "median"),
            monetary_value=("monetary_value", "median"),
            size=("recency", "count"),
        )

        def name_cluster(row):
            if row["recency"] > 100:
                return "Inactive"
            elif row["frequency"] > 10 or row["monetary_value"] > 1000:
                return "Platinum Customers"
            elif row["frequency"] < 2:
                return "New Customers"
            else:
                return "Gold Customers"

        rfm_summary["name"] = rfm_summary.apply(name_cluster, axis=1)
        df_rfm["cluster_name"] = df_rfm["cluster"].map(rfm_summary["name"])
        rfm_summary = df_rfm.groupby("cluster_name").agg(
            recency=("recency", "median"), frequency=("frequency", "median"),
            monetary_value=("monetary_value", "median"),
            size=("recency", "count"),
        ).sort_values("size", ascending=True)
        print("\n--- Customer Segments Summary ---")
        print(rfm_summary)

        print("\nGenerating visualizations...")
        sns.set_style("white")

        # --- Taille des segments ---
        plt.figure(figsize=(15, 6))
        ax1 = sns.barplot(
            x=rfm_summary["size"], y=rfm_summary.index, palette="pastel")
        ax1.set_title("Number of Customers by Segment")
        ax1.set_xlabel("number of customers")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        for index, value in enumerate(rfm_summary["size"]):
            ax1.text(value, index, f' {value}', va='center')
        plt.show()

        # --- Profil des segments ---
        plt.figure(figsize=(10, 6))
        rfm_summary["recency_months"] = rfm_summary["recency"] / 30.0

        ax2 = sns.scatterplot(
            data=rfm_summary, x="recency_months", y="frequency",
            size="monetary_value", hue=rfm_summary.index,
            sizes=(500, 5000), palette="pastel", legend=False,
            alpha=0.7)
        ax2.set_title("Customer Segment Profiles")
        ax2.set_xlabel("Median Recency (month)")
        ax2.set_ylabel("Median Frequency")
        ax2.set_xlim(left=-0.5, right=4)
        ax2.set_ylim(bottom=0, top=25)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        for i, row in rfm_summary.iterrows():
            ax2.text(
                row["recency_months"], row["frequency"] + 1.5,
                f'Average "{i}": {row["monetary_value"]:.0f}₳',
                ha="center")
        plt.show()

        # --- Visualisation du Clustering ---
        sns.set_style("darkgrid")
        plt.figure(figsize=(12, 8))

        ax3 = sns.scatterplot(
            x=rfm_scaled[:, 1], y=rfm_scaled[:, 2],
            hue=df_rfm["cluster"], palette="bright",
            alpha=0.6, legend="full", s=100)
        centroids = kmeans.cluster_centers_
        ax3.scatter(centroids[:, 1], centroids[:, 2],
                    s=250, c="yellow", edgecolor="black", label="Centroids")
        ax3.set_title("Clusters of Customers")
        ax3.set_xlabel("Frequency")
        ax3.set_ylabel("Monetary Value")
        ax3.legend()
        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    create_customer_segments(db_params, table_name)
