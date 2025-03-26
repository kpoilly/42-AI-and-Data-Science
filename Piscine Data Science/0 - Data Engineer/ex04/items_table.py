import os
import sys
import pandas as pd
from sqlalchemy import create_engine, Table, Column, \
     Integer, String, Float, DateTime, MetaData


DATABASE_URL = "postgresql://kpoilly:mysecretpassword@localhost:5432/piscineds"
FOLDER = "/home/kpoilly/sgoinfre/subject/item/"


def csv_to_table(engine, csv_path):
    """
    Creaes a PostgreSQL table from a given csv
    """
    filename = os.path.basename(csv_path)
    tablename = 'items'

    try:
        df = pd.read_csv(csv_path)
        metadata = MetaData()

        columns = []
        columns_types = {}

        df['Datetime'] = str(pd.Timestamp('now'))
        cols = df.columns.tolist()
        cols = ['Datetime'] + [col for col in cols if col != 'Datetime']
        df = df[cols]

        for col in df.columns:
            try:
                numeric_series = pd.to_numeric(df[col], errors='raise')
                if numeric_series.astype(float)\
                   .apply(lambda x: x.is_integer()).all():
                    columns_types[col] = Integer
                else:
                    columns_types[col] = Float
            except ValueError:
                try:
                    pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S UTC',
                                   errors='raise')
                    columns_types[col] = DateTime
                except ValueError:
                    columns_types[col] = String

        for col in df.columns:
            columns.append(Column(col, columns_types[col]))

        Table(tablename, metadata, *columns)
        metadata.create_all(engine)
        df.to_sql(tablename, engine, if_exists='append', index=False)
        print(f"Table {tablename} created from {filename}.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


def main():
    engine = create_engine(DATABASE_URL)

    if not os.path.exists(FOLDER):
        print(f"Error: Cannot found Customer folder at {FOLDER}.",
              file=sys.stderr)
        return

    for csv in os.listdir(FOLDER):
        if csv.endswith('.csv'):
            csv_to_table(engine, os.path.join(FOLDER, csv))


if __name__ == "__main__":
    main()
