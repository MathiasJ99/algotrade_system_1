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
    start=datetime.now() - timedelta(minutes=360),
    end=datetime.now()
    
)

# Fetch quotes
crypto_bars = crypto_historic_client.get_crypto_bars(crypto_request).df
#crypto_bars.index = pd.to_datetime(crypto_bars.index)
#crypto_bars = crypto_bars.resample('1T').asfreq()
print(crypto_bars.head())
crypto_bars.to_csv('crypto_bars.csv', index=True)

''' 
# REAL TIME CRYPTO DATA STREAM
# Define callbacks
async def handle_quote(quote):
    print(f"Quote: {quote}")

async def handle_trade(trade):
    print(f"Trade: {trade}")

async def handle_bar(bar):
    print(f"Bar: {bar}")


crypto_stream = CryptoDataStream(os.getenv("api_key"), os.getenv("secret_key"))
crypto_stream.subscribe_bars(handle_bar, "BTC/USD")
crypto_stream.subscribe_trades(handle_trade, "BTC/USD")
crypto_stream.subscribe_quotes(handle_quote, "BTC/USD")

crypto_stream.run()


'''