import pandas as pd
import os

def check_if_already_analyzed(filename, csv_file='output.csv'):
    """
    Check if a PDF has already been analyzed by looking for its name in the CSV file.

    Args:
        filename (str): The name of the PDF file to check.
        csv_file (str): The path to the CSV file.

    Returns:
        bool: True if the PDF has already been analyzed, False otherwise.
    """
    if not os.path.exists(csv_file):
        return False
    
    df = pd.read_csv(csv_file)
    return filename in df['filename'].values

def push_csv_info(number, name, price, date, filename, csv_file='output.csv'):
    """
    Pushes the provided information into a CSV file.

    Args:
        number (str): The bill number.
        name (str): The name of the person who receives the bill.
        price (str): The price or cost mentioned in the document.
        date (str): The date mentioned in the document.
        filename(str): file where the info are extracted
        csv_file (str): The path to the CSV file. Default is 'output.csv'.
    """

    data = {
        'number': number,
        'name': name,
        'price': price,
        'filename': filename,
        'date': date
    }

    df = pd.DataFrame([data])

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False)

    print(f"Information pushed to {csv_file}: {data}")
