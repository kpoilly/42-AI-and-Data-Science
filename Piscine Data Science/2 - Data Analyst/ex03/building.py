import sys

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Settings ---
db_params = {
    "host": "localhost",
    "database": "piscineds",
    "user": "kpoilly",
    "password": "mysecretpassword",
}
table_name = "customers"


def generate_rfm_histograms(db_params, table_name):
    """
    Calcule la fréquence d'achat et la valeur monétaire pour chaque client
    et génère des histogrammes pour visualiser leurs distributions.
    """
    conn = None
    print("Starting Frequency-Monetary analysis...")

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the PostgreSQL database.")

        query_rfm = f"""
            SELECT
                user_id,
                COUNT(*) AS frequency,
                SUM(price) AS monetary_value
            FROM
                {table_name}
            WHERE
                event_type = 'purchase'
            GROUP BY
                user_id
            HAVING
                SUM(price) < 225;
        """
        df_rfm = pd.read_sql_query(query_rfm, conn)
        if df_rfm.empty:
            print("No valid purchase data found to generate histograms.")
            return

        print("Generating histograms...")
        sns.set_style("darkgrid")

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("Customer Segmentation Analysis", fontsize=16)

        # --- Distribution de la Fréquence ---
        ax1 = axes[0]
        sns.histplot(
            data=df_rfm,
            x="frequency",
            ax=ax1,
            binwidth=8,
            color="lightsteelblue",
        )
        ax1.set_title("Distribution of Order Frequency")
        ax1.set_xlabel("frequency")
        ax1.set_ylabel("customers")
        ax1.set_xticks(range(0, 39, 10))
        ax1.set_xlim(0, 40)

        # --- Distribution de la Valeur Monétaire ---
        ax2 = axes[1]
        sns.histplot(
            data=df_rfm,
            x="monetary_value",
            ax=ax2,
            bins=5,
            color="lightsteelblue",
        )
        ax2.set_title("Distribution of Monetary Value")
        ax2.set_xlabel("monetary value in ₳")
        ax2.set_ylabel("customers")
        ax2.set_xticks(range(0, 249, 50))
        ax2.set_xlim(0, 249)

        plt.tight_layout()
        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    generate_rfm_histograms(db_params, table_name)
