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


def generate_price_boxplots(db_params, table_name):
    """
    Analyse la distribution des prix d'achat, affiche les statistiques
    et génère une série de diagrammes en boîte (box plots).
    """
    conn = None
    print("Starting price distribution analysis...")

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the PostgreSQL database.")

        query_item_prices = f"""
            SELECT
                price
            FROM
                {table_name}
            WHERE
                event_type = 'purchase';
        """
        print("Fetching individual item prices...")
        df_prices = pd.read_sql_query(query_item_prices, conn)
        if df_prices.empty:
            print("No purchase events found. Aborting.")
            return

        print("\n--- Price Statistics for All Purchased Items ---")
        pd.options.display.float_format = "{:,.6f}".format
        print(df_prices["price"].describe().to_string())

        query_avg_basket_per_user = f"""
            WITH UserBaskets AS (
                SELECT
                    user_id,
                    SUM(price) AS basket_price
                FROM
                    {table_name}
                WHERE
                    event_type = 'purchase'
                GROUP BY
                    user_id, user_session
                HAVING
                    SUM(price) >= 0
            )
            SELECT
                AVG(basket_price) AS avg_user_basket_price
            FROM
                UserBaskets
            GROUP BY
                user_id;
        """
        print("\nFetching total basket prices per user...")
        df_baskets = pd.read_sql_query(query_avg_basket_per_user, conn)

        print("Generating box plots...")
        sns.set_style("darkgrid")
        fig, axes = plt.subplots(3, 1, figsize=(8, 12))
        fig.suptitle("Analysis of Purchase Prices", fontsize=16)

        # --- Prix de tous les articles (avec outliers) ---
        ax1 = axes[0]
        sns.boxplot(data=df_prices, x="price", ax=ax1)
        ax1.set_title("Distribution of All Item Prices (including outliers)")

        # --- Prix des articles "normaux" ---
        ax2 = axes[1]
        df_prices_filtered = df_prices[
            (df_prices["price"] >= 0) & (df_prices["price"] <= 12.5)]
        sns.boxplot(
            data=df_prices_filtered, x="price", ax=ax2, color="mediumseagreen")
        ax2.set_title("Distribution of Item Prices (0 to 12.5)")

        # --- Prix des paniers par session ---
        ax3 = axes[2]
        sns.boxplot(
            data=df_baskets, x="avg_user_basket_price",
            ax=ax3, color="skyblue")
        ax3.set_title("Average Basket Price per User")
        ax3.set_xlim(-50, 200)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    generate_price_boxplots(db_params, table_name)
