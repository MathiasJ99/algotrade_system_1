import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
import pandas as pd

from alpaca.data.historical import StockHistoricalDataClient , CryptoHistoricalDataClient
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import CryptoBarsRequest

load_dotenv()
# Initialize clients
stock_historic_client = StockHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))
crypto_historic_client = CryptoHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))     

# Set request parameters
crypto_request = CryptoBarsRequest(
    symbol_or_symbols="BTC/USD",
    timeframe=TimeFrame.Minute,
    start=datetime.now() - timedelta(minutes=120960), # 3 weeks
    end=datetime.now()
)

# Fetch quotes 
crypto_df = crypto_historic_client.get_crypto_bars(crypto_request).df
print(crypto_df.head())
print(crypto_df.tail())
print(f"finished fetching data, shape is {crypto_df.shape}")

# Save to CSV
crypto_df.to_csv('crypto_data_latest.csv', index=True)
print("Data saved to crypto_data_latest.csv")
