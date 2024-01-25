import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np

# Define entities and call functions
url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
csv_path = "exchange_rate.csv"
output_path = "./Largest_banks_data.csv"
table_name = "Largest_banks"
query_statement = "SELECT * FROM Largest_banks"
query_statement1 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
query_statement2 = "SELECT Name from Largest_banks LIMIT 5"
db_name = "Banks.db"


# Log progress function
def log_progress(message):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{time_stamp} : {message}\n"
    with open("code_log.txt", "a") as log_file:
        log_file.write(log_entry)


def extract(url):
    # Send a GET request to the URL
    request = requests.get(url)

    # Check if the request was successful
    if request.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(request.text, "html.parser")

        # Find the first table in the HTML content
        data = soup.find_all('table')[0]

        # Extract table headers
        headers = data.find_all('th')
        heading = [titles.text.strip() for titles in headers]

        # Create an empty DataFrame with the extracted headers
        df = pd.DataFrame(columns=heading)

        # Extract table rows and populate the DataFrame
        rows = data.find_all('tr')[1:]
        for row in rows:
            values = row.find_all('td')
            individual_values = [data.text.strip() for data in values]
            length = len(df)
            df.loc[length] = individual_values

        # Rename the 'Market cap(US$ billion)' column to 'Market cap'
        df.rename(columns={'Market cap(US$ billion)': 'MC_USD_Billion'}, inplace=True)

        # Convert 'Market cap' column to float
        df['MC_USD_Billion'] = pd.to_numeric(df['MC_USD_Billion'], errors='coerce').astype('float')
        log_progress("Data extraction complete. Initiating Transformation process")
        return df
    else:
        print(f"Failed to retrieve data. Status code: {request.status_code}")
        return None

        print(df)

# Transform function
def transform(df, csv_path):
    # Read exchange rate CSV file into a DataFrame
    exchange_rates = pd.read_csv(csv_path)

    # Convert exchange rates to a dictionary
    exchange_rate_dict = exchange_rates.set_index('Currency').to_dict()['Rate']

    # Add columns to the DataFrame
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rate_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rate_dict['INR'], 2) for x in df['MC_USD_Billion']]

    log_progress("Data transformation complete. Initiating Loading process")
    return df

# Load to CSV function
def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    log_progress("Data saved to CSV file")

def load_to_db(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    log_progress("Data loaded to Database as a table, Executing queries")

# Run Query function
def run_query(query_statement, db_name):
    conn = sqlite3.connect(db_name)
    result = pd.read_sql_query(query_statement, conn)
    print(result)
    log_progress("Print the contents of the entire table")

# Run Query function
def run_query1(query_statement1, db_name):
    conn = sqlite3.connect(db_name)
    result1 = pd.read_sql_query(query_statement, conn)
    print(result1)
    log_progress("Print the average market capitalization of all the banks in Billion USD")

# Run Query function
def run_query2(query_statement2, db_name):
    conn = sqlite3.connect(db_name)
    result2 = pd.read_sql_query(query_statement, conn)
    print(result2)
    log_progress("Print only the names of the top 5 banks")

# Call functions
data_frame = extract(url)
data_frame = transform(data_frame, csv_path)
load_to_csv(data_frame, output_path)
load_to_db(data_frame, db_name, table_name)
run_query(query_statement, db_name)
run_query1(query_statement1, db_name)
run_query2(query_statement2, db_name)
