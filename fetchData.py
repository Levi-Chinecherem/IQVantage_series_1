# fetchData.py
import requests
import pandas as pd
from datetime import datetime
import os

# Function to fetch Binance data
def fetch_binance_data(symbol, start_time, end_time):
    # Define your Binance API URL and parameters
    binance_api_url = "https://api.binance.com/api/v3/klines"
    interval = "1h"  # You can change the interval as needed

    # Convert date strings to timestamps
    start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%d").timestamp()) * 1000
    end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%d").timestamp()) * 1000

    # Define query parameters
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_timestamp,
        "endTime": end_timestamp,
        "limit": 1000  # Adjust the limit as needed
    }

    try:
        # Make a GET request to the Binance API
        response = requests.get(binance_api_url, params=params)
        data = response.json()
        
        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        
        # Extract and convert timestamp to a human-readable format
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        return df

    except Exception as e:
        print(f"Error fetching Binance data: {str(e)}")
        return None

# Function to clean the data
def clean_data(data):
    # Convert timestamp column to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    # Handle missing data (fill with zeros in this example)
    data.fillna(0, inplace=True)

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # Convert the 'close' column to numeric type, handling non-numeric values
    data['close'] = pd.to_numeric(data['close'], errors='coerce')

    # Remove rows with non-numeric 'close' values
    data = data[data['close'].notna()]

    # Remove outliers (example: values more than 3 standard deviations from the mean)
    data = data[(data['close'] < data['close'].mean() + 3 * data['close'].std()) & 
                (data['close'] > data['close'].mean() - 3 * data['close'].std())]

    # Rename columns for clarity (you can customize these names)
    data.rename(columns={
        'timestamp': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume',
        'number_of_trades': 'Trades'
    }, inplace=True)

    return data

# Function to save the cleaned data
def save_clean_data(data, filename):
    # Define the folder path
    folder_path = 'data'
    
    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the cleaned data to a CSV file inside the folder
    data.to_csv(os.path.join(folder_path, f'{filename}.csv'), index=False)

def main():
    symbol = "BTCUSDT"
    start_time = "2023-01-01"
    end_time = "2023-01-31"
    
    # Fetch Binance data
    data = fetch_binance_data(symbol, start_time, end_time)
    
    if data is not None:
        # Clean the data
        cleaned_data = clean_data(data)
        
        # Save the clean data
        save_clean_data(cleaned_data, f"cleaned_{symbol}_{start_time}_{end_time}")

if __name__ == "__main__":
    main()
