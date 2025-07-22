import os
from alpaca.trading.stream import TradingStream
from dotenv import load_dotenv
from alpaca.trading.requests import LimitOrderRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
from alpaca.data.live.crypto import CryptoDataStream
from StrategyDevelopment import get_best_params

#Setting up env vars and clients
load_dotenv()
trading_client = TradingClient(api_key = os.getenv("api_key"),secret_key = os.getenv("secret_key"),paper = True)
crypto_stream = CryptoDataStream(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))
crypto_historic_client = CryptoHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))     

def get_latest_crypto_data(symbol):
    crypto_request = CryptoBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=datetime.now() - timedelta(minutes=120960), # 3 weeks
        end=datetime.now()
    )
    # Fetch quotes 
    crypto_df = crypto_historic_client.get_crypto_bars(crypto_request).df
    return crypto_df

def get_best_params():
    return get_best_params()

params = get_best_params()
df = get_latest_crypto_data("BTC/USD")


def calculate_SMA(short, long, position_size):
    if len(df) < long:
        return None

    short_sma = pd.Series(df['close']).ewm(span=short, adjust=False).mean()
    long_sma = pd.Series(df['close']).ewm(span=long, adjust=False).mean()

    if short_sma[-2] < long_sma[-2]:
        if short_sma[-1] > long_sma[-1]:
            #check if enough funds to buy
            buy_crypto("BTC/USD", position_size)

    elif short_sma[-2] > long_sma[-2]:
        if short_sma[-1] < long_sma[-1]:
            if self.position:
                #check if open position to sell
                sell_crypto("BTC/USD", position_size)

def buy_crypto(symbol, qty):

    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )

    market_order = trading_client.submit_order(order)

def sell_crypto(symbol, qty):

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
    print(f"Bar: {bar}")
    df = df.append(bar)
    calculate_SMA(params['n_short'], params['n_long'], 0.1)


crypto_stream.subscribe_bars(handle_bar, "BTC/USD")
#crypto_stream.subscribe_trades(handle_trade, "BTC/USD")
#crypto_stream.subscribe_quotes(handle_quote, "BTC/USD")
crypto_stream.run()

