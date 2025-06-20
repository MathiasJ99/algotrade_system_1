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