import pandas as pd
import os

def push_csv_info(number, name, price, date, csv_file='output.csv'):
    """
    Pushes the provided information into a CSV file.

    Args:
        number (str): The bill number.
        name (str): The name of the person who receives the bill.
        price (str): The price or cost mentioned in the document.
        date (str): The date mentioned in the document.
        csv_file (str): The path to the CSV file. Default is 'output.csv'.
    """

    data = {
        'number': number,
        'name': name,
        'price': price,
        'date': date
    }

    df = pd.DataFrame([data])

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False)

    print(f"Information pushed to {csv_file}: {data}")
