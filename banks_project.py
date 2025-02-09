import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
import datetime as dt

url = 'https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks'
csv_output = "Largest_banks_data.csv"
database = 'Banks.db'
table_name = 'Largest_banks'
log_file = 'code_log.txt'
columns_extract = ['Name', 'MC_USD_Billion']
final_columns = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
exchange_rate = 'exchange_rate.csv'
bank_data = []
query_statement =['SELECT * FROM Largest_banks','SELECT AVG(MC_GBP_Billion) FROM Largest_banks','SELECT Name from Largest_banks LIMIT 5']

# Log progress
def log_progress(message):
    with open(log_file, 'a') as file:
        file.write(f'{dt.datetime.now()}:{message}\n')

# Extract data from website and return a DataFrame
def extract(url, table_attribs):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        if not table:
            return ("not find table")
        for row in table.find_all('tr'):
            cell = row.find_all('td')
            if len(cell) >= 2:
                name = cell[1].text.strip()
                mc_usd = cell[2].text.strip()
                bank_data.append({
                    table_attribs[0]: name,
                    table_attribs[1]: mc_usd
                })
        df = pd.DataFrame(bank_data)
        df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)
        log_progress('Data extraction complete. Initiating Transformation process')
    except requests.exceptions.RequestException as e:
        print(f"{str(e)}")
        exit(1)
    return df

# Transform data to add columns for GBP, EUR and INR
def transform(df, csv_path):
    df_exchange_rate = pd.read_csv(csv_path)
    dict = df_exchange_rate.set_index(df_exchange_rate.iloc[:,0]).to_dict()[df_exchange_rate.columns[1]]
    df['MC_GBP_Billion'] = [np.round(x*dict['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*dict['EUR'],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*dict['INR'],2) for x in df['MC_USD_Billion']]
    log_progress('Data transformation complete. Initiating Loading process')
    return df

 # Load data to CSV file
def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    log_progress('Data saved to CSV file')
    

 # Load data to Database 
def load_to_db(df, sql_connection, table_name):
    try:
        with sqlite3.connect(sql_connection) as conn:
            log_progress('SQL Connection initiated')  
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists='replace',
                index=False,
                dtype={
                    'Name': 'TEXT',
                    'MC_USD_Billion': 'FLOAT',
                    'MC_GBP_Billion': 'FLOAT',
                    'MC_EUR_Billion': 'FLOAT',
                    'MC_INR_Billion': 'FLOAT'
                }
            )
        log_progress('Data loaded to Database as a table, Executing queries')
        log_progress('Server Connection closed')
        print(f"Save {table_name}")
    except sqlite3.Error as e:
        print(f"Error: {str(e)}")
        
 # Run queries on Database       
def run_query(query_statement, sql_connection):
    log_progress('Data loaded to Database as a table, Executing queries')
    try:
        with sqlite3.connect(sql_connection) as conn:
            cursor = conn.cursor()
            log_progress('SQL Connection initiated')
            cursor.execute(query_statement[0])
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            cursor.execute(query_statement[1])
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            cursor.execute(query_statement[2])
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            log_progress('Process Complete')
            log_progress('Server Connection closed')

    except sqlite3.Error as e:
        print(f"Error: {str(e)}")

    
print(extract(url, columns_extract))
print(transform(extract(url, columns_extract),exchange_rate))
load_to_csv(transform(extract(url, columns_extract),exchange_rate), csv_output)
load_to_db(transform(extract(url, columns_extract),exchange_rate), database, table_name)
run_query(query_statement,database)