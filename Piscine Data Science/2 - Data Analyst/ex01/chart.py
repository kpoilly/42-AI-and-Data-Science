import sys

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


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
    Se connecte à la base de données, analyse les données d'achat
    sur une période donnée et génère un tableau de bord de 3 graphiques.
    """
    conn = None
    print("Starting user event analysis...")

    start_date = "2022-10-01"
    end_date = "2023-03-01"

    try:
        conn = psycopg2.connect(**db_params)
        print("Successfully connected to the database.")

        query_daily_customers = f"""
            SELECT
                DATE(event_time) AS purchase_date,
                COUNT(DISTINCT user_id) AS daily_customers
            FROM {table_name}
            WHERE
                event_type = 'purchase'
                AND event_time >= '{start_date}' AND event_time < '{end_date}'
            GROUP BY purchase_date
            ORDER BY purchase_date;
        """

        query_monthly_sales = f"""
            SELECT
                DATE_TRUNC('month', event_time) AS purchase_month,
                SUM(price) / 1000000.0 AS total_sales_in_millions
            FROM {table_name}
            WHERE
                event_type = 'purchase'
                AND event_time >= '{start_date}' AND event_time < '{end_date}'
            GROUP BY purchase_month
            ORDER BY purchase_month;
        """

        query_avg_spend = f"""
            SELECT
                DATE(event_time) AS purchase_date,
                SUM(price) / COUNT(DISTINCT user_id) AS avg_spend_per_customer
            FROM {table_name}
            WHERE
                event_type = 'purchase'
                AND event_time >= '{start_date}' AND event_time < '{end_date}'
            GROUP BY purchase_date
            ORDER BY purchase_date;
        """

        print("Fetching data...")
        df_daily_customers = pd.read_sql_query(
            query_daily_customers, conn, parse_dates=["purchase_date"]
        )
        df_monthly_sales = pd.read_sql_query(
            query_monthly_sales, conn, parse_dates=["purchase_month"]
        )
        df_avg_spend = pd.read_sql_query(
            query_avg_spend, conn, parse_dates=["purchase_date"]
        )

        print("Generating dashboard...")
        sns.set_style("darkgrid")
        sns.set_palette("pastel")
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))
        fig.suptitle("Purchase Analysis (Oct 2022 - Feb 2023)", fontsize=20)

        # --- Nombre de clients par jour ---
        ax1 = axes[0]
        sns.lineplot(
            data=df_daily_customers, x="purchase_date",
            y="daily_customers", ax=ax1)
        ax1.set_ylabel("Number of customers")
        ax1.set_xlabel("")
        ax1.set_title("Daily Unique Customers", fontsize=14)

        # --- Ventes totales par mois ---
        ax2 = axes[1]
        df_monthly_sales["month_label"] = df_monthly_sales["purchase_month"]\
            .dt.strftime("%b")
        sns.barplot(
            data=df_monthly_sales,
            x="month_label",
            y="total_sales_in_millions",
            ax=ax2,
            color="lightsteelblue",
        )
        ax2.set_ylabel("total sales in million of ₳")
        ax2.set_xlabel("month")
        ax2.set_title("Total Monthly Sales", fontsize=14)

        # --- Dépense moyenne par client ---
        ax3 = axes[2]
        ax3.fill_between(
            df_avg_spend["purchase_date"],
            df_avg_spend["avg_spend_per_customer"],
            alpha=0.5,
            color="lightsteelblue",
        )
        ax3.set_ylabel("average spend/customers in ₳")
        ax3.set_xlabel("")
        ax3.set_title("Daily Average Spend per Customer", fontsize=14)
        ax3.set_ylim(bottom=0)

        for ax in [ax1, ax3]:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
            ax.set_xlim(
                [df_daily_customers["purchase_date"].min(),
                 df_daily_customers["purchase_date"].max()])

        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        plt.show()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError: {error}", file=sys.stderr)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
        print("Analysis process finished.")


if __name__ == "__main__":
    analyze_user_events(db_params, table_name)
