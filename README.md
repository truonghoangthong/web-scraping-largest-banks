# Largest Bank Data Scraping

## Project Overview

I threw this project together to dig into data about the world’s biggest banks by scraping their market capitalization from Wikipedia. My goal was to pull the data, convert it into different currencies using exchange rates, and organize it into a CSV and a SQLite database.

This project does a few neat things:

- Grabs market cap data for banks like JPMorgan Chase and HDFC Bank from Wikipedia.
- Converts those numbers into GBP, EUR, and INR based on exchange rates.
- Saves the results in a CSV file and a SQLite database.
- Runs some SQL queries to poke around the data, like finding the average market cap or listing the top banks.

## Dataset

All the data is tucked away in the `largest_bank_data/` folder. Here’s the breakdown:

- **Input**:
  - `exchange_rate.csv`: Has exchange rates for USD to GBP (0.8), EUR (0.93), and INR (82.95).
- **Output**:
  - `Largest_banks_data.csv`: The scraped data with bank names and market caps in USD, GBP, EUR, and INR (e.g., JPMorgan Chase at $432.92B USD, £346.34B GBP).
  - `Banks.db`: A SQLite database with a `Largest_banks` table holding the same data.
  - `code_log.txt`: A log file tracking what the script was up to at each step.

The data comes from an archived Wikipedia page: List of largest banks.

## Analysis

I used Python to scrape, tweak, and store the data. Here’s how it all came together:

1. **Web Scraping**:
   - Pulled bank names and market caps (in USD billions) from a Wikipedia table using `BeautifulSoup`.
2. **Data Transformation**:
   - Loaded exchange rates from `exchange_rate.csv` and used them to convert market caps into GBP, EUR, and INR (e.g., Bank of America’s $231.52B USD became €215.31B EUR).
   - Rounded everything to two decimals to keep it tidy.
3. **Data Storage**:
   - Saved the transformed data to `Largest_banks_data.csv`, with banks like HSBC Holdings and China Construction Bank included.
   - Loaded it into a SQLite database (`Banks.db`) as a table called `Largest_banks`.
   - Kept a log of every step in `code_log.txt` to stay on top of things.
4. **SQL Queries**:
   - Ran a few queries on the database:
     - Grabbed all the bank records (like Morgan Stanley’s $140.83B USD market cap).
     - Worked out the average market cap in GBP.
     - Listed the names of the top 5 banks, like JPMorgan Chase and Wells Fargo.
