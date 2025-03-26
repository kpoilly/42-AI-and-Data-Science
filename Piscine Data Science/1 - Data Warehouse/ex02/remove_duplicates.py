from sqlalchemy import create_engine, text


query = """
WITH RowNumCTE AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY kpoilly, kpoilly@42.student.fr
                           ORDER BY ) AS rn
    FROM
        Customers
)
DELETE FROM Customers
WHERE customerid IN (SELECT customerid FROM RowNumCTE WHERE rn > 1);
"""


def main():
    try:
        engine = create_engine('postgresql://kpoilly:mysecretpassword\
@5432/piscineds')
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
            print("Duplicates rows deleted from Customers")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit()
    engine.dispose()


if __name__ == "__main__":
    main()
