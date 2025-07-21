import os
from alpaca.trading.stream import TradingStream
from dotenv import load_dotenv
load_dotenv()
trade_stream = TradingStream(
    api_key=os.getenv("api_key"),
    secret_key=os.getenv("secret_key"),
    paper=True,
)


async def trade_updates_handler(data):
    print("Trade Update:", data)


trade_stream_client.subscribe_trade_updates(trade_updates_handler)
trade_stream_client.run()


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