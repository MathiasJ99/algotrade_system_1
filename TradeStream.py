import os
import pandas as pd
import asyncio 
from datetime import datetime, timedelta
from alpaca.trading.stream import TradingStream
from dotenv import load_dotenv
from alpaca.trading.requests import LimitOrderRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
from alpaca.data.live.crypto import CryptoDataStream
from StrategyDevelopment import get_best_params
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

#Setting up env vars and clients
load_dotenv()
trading_client = TradingClient(api_key = os.getenv("api_key"),secret_key = os.getenv("secret_key"),paper = True)
crypto_stream = CryptoDataStream(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))
crypto_historic_client = CryptoHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))   

print("#################")
print("RUNNING STREAM")
print("#################")

def get_latest_crypto_data(symbol):
    crypto_request = CryptoBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=datetime.now() - timedelta(minutes=12960), # 3 weeks
        end=datetime.now()
    )
    # Fetch quotes 
    crypto_df = crypto_historic_client.get_crypto_bars(crypto_request).df
    return crypto_df

def format_df(df):
    df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
    #df["timestamp"] = pd.to_datetime(df["timestamp"])
    #df.set_index("timestamp", inplace=True)
    return df

#GLOBAL VARS
params = get_best_params()
df = get_latest_crypto_data("BTC/USD")
df = format_df(df).reset_index()
position_open = False

def calculate_SMA(short, long, position_size):
    print("Calculating SMA")

    global position_open
    if len(df) < long:
        return None

    short_sma = pd.Series(df['Close']).ewm(span=short, adjust=False).mean()
    long_sma = pd.Series(df['Close']).ewm(span=long, adjust=False).mean()

    if short_sma.iloc[-2] < long_sma.iloc[-2]:
        if short_sma.iloc[-1] > long_sma.iloc[-1]:
            #check if enough funds to buy
            buy_crypto("BTC/USD", position_size)
            position_open = True
            

    elif short_sma.iloc[-2] > long_sma.iloc[-2]:
        if short_sma.iloc[-1] < long_sma.iloc[-1]:
            if position_open:
                #check if open position to sell
                curr_qty = get_current_btc_qty()
                sell_crypto("BTC/USD", float(curr_qty-0.000001))
                position_open = False
                
    
def get_current_btc_qty():
    btc_usd_position = trading_client.get_open_position(symbol_or_asset_id="BTCUSD")
    return float(btc_usd_position.qty_available)

def buy_crypto(symbol, qty):
    print(f"Buying {qty} of {symbol}")
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )

    market_order = trading_client.submit_order(order)

def sell_crypto(symbol, qty):
    print(f"Selling {qty} of {symbol}")
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC
    )

    market_order = trading_client.submit_order(order)


#Async functions to handle real time  DATA STREAM
async def handle_quote(quote):
    print(f"Quote: {quote}")

async def handle_trade(trade):
    print(f"Trade: {trade}")

async def handle_bar(bar):
    global df
    global position_open

    new_row_df = pd.DataFrame({
        'timestamp': [bar.timestamp],
        'open': [bar.open],
        'high': [bar.high],
        'low': [bar.low],
        'close': [bar.close],
        'volume': [bar.volume],
        'trade_count': [bar.trade_count],
        'vwap': [bar.vwap]
    })

    new_row_df = format_df(new_row_df)
    df = pd.concat([df, new_row_df], axis =0).reset_index(drop=True)
    
    print("NEW BAR ADDED")
    #print(df.tail())

    calculate_SMA(params['n_short'], params['n_long'], 0.4)
    '''
    if position_open:
        curr_qty = get_current_btc_qty()
        sell_crypto("BTC/USD", float(curr_qty-0.000001))
        position_open = False
    else:
        buy_crypto("BTC/USD", 0.1)
        position_open = True

    '''

crypto_stream.subscribe_bars(handle_bar, "BTC/USD")
#crypto_stream.subscribe_trades(handle_trade, "BTC/USD")
#crypto_stream.subscribe_quotes(handle_quote, "BTC/USD")
crypto_stream.run()
