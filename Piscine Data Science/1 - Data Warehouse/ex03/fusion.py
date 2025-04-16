import csv
import pandas as pd
from sqlalchemy import create_engine, text, inspect


def main():
    print("Adding item.csv to customers...")
    try:
        engine = create_engine('postgresql://kpoilly:mysecretpassword@localhost:5432/piscineds')
        inspector = inspect(engine)
        customer_columns = [col['name'] for col in inspector.get_columns('customers')]

        with open('/home/kpoilly/sgoinfre/subject/item/item.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            with engine.connect() as connection:
                for row in reader:
                    product_id = row.get('product_id')
                    insert_columns = []
                    insert_values = {}

                    if 'Datetime' in customer_columns:
                        insert_columns.append('"Datetime"')
                        insert_values['Datetime'] = str(pd.Timestamp('now'))

                    if 'event_time' in customer_columns:
                        insert_columns.append('event_time')
                        insert_values['event_time'] = insert_values['Datetime']

                    if 'product_id' in customer_columns:
                        insert_columns.append('product_id')
                        insert_values['product_id'] = product_id if product_id else None

                    if 'price' in customer_columns:
                        insert_columns.append('price')
                        insert_values['price'] = None

                    if 'user_id' in customer_columns:
                        insert_columns.append('user_id')
                        insert_values['user_id'] = None

                    if 'user_session' in customer_columns:
                        insert_columns.append('user_session')
                        insert_values['user_session'] = None

                    if insert_columns:
                        columns_str = ', '.join(insert_columns)
                        placeholders_str = ', '.join([f':{key}' for key in insert_values.keys()])
                        insert_query = text(f"""
                            INSERT INTO customers ({columns_str})
                            VALUES ({placeholders_str})
                        """)
                        connection.execute(insert_query, insert_values)

                connection.commit()
                print("item.csv added to customers table.")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit()
    engine.dispose()


if __name__ == "__main__":
    main()