# Web Scraping and Data Transformation

This Python script performs web scraping on a Wikipedia page to extract information about the largest banks. The extracted data is then transformed and loaded into a SQLite database for further analysis.

## Code Overview

### 1. Log Progress Function
The `log_progress` function logs messages with timestamps to a file (`code_log.txt`) to keep track of the code execution progress.

### 2. Data Extraction (extract function)
The `extract` function sends a GET request to a specified URL, extracts data from the first table, and converts it into a Pandas DataFrame. The 'Market cap' column is cleaned and converted to a float.

### 3. Data Transformation (transform function)
The `transform` function reads exchange rate data from a CSV file, converts exchange rates to a dictionary, and adds columns to the DataFrame for market capitalization in GBP, EUR, and INR. Rounding is applied to the values.

### 4. Load to CSV (load_to_csv function)
The `load_to_csv` function saves the DataFrame to a CSV file (`Largest_banks_data.csv`).

### 5. Load to Database (load_to_db function)
The `load_to_db` function connects to a SQLite database (`Banks.db`) and loads the DataFrame as a table. If the table already exists, it is replaced.

### 6. Call Functions
The script calls the functions in the following order:
1. `extract`: Extracts data from the Wikipedia page.
2. `transform`: Transforms the data by converting market capitalization to GBP, EUR, and INR.
3. `load_to_csv`: Saves the transformed data to a CSV file.
4. `load_to_db`: Loads the transformed data into a SQLite database.
5. `run_query`, `run_query1`, `run_query2`: Executes and prints the results of specific SQL queries.

## Usage
To run this script, make sure you have the required libraries installed (`pandas`, `sqlite3`, `requests`, `bs4`, `numpy`). Additionally, provide the correct URL and CSV path in the script.