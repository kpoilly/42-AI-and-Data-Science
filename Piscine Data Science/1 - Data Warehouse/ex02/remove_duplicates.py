from sqlalchemy import create_engine, text, inspect


query = """
WITH RowNumCTE AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY {columns_list} ORDER BY (SELECT NULL)) AS rn
    FROM
        customers
)
DELETE FROM customers
WHERE (
    {columns_list}
) IN (
    SELECT
        {columns_list}
    FROM
        RowNumCTE
    WHERE
        rn > 1
);
"""


def main():
    print("Deleting duplicate rows from customers...")
    try:
        engine = create_engine("postgresql://kpoilly:mysecretpassword@localhost:5432/piscineds")
        inspector = inspect(engine)
        columns = inspector.get_columns('customers')
        column_names = [f'"{col["name"]}"' for col in columns]
        columns_list = ', '.join(column_names)

        with engine.connect() as connection:
            connection.execute(text(query.format(columns_list=columns_list)))
            connection.commit()
            print("Duplicate rows deleted from customers")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit()
    engine.dispose()


if __name__ == "__main__":
    main()
