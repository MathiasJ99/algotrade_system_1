import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import alpaca

from alpaca.data.historical.option import OptionHistoricalDataClient,OptionLatestQuoteRequest 
from alpaca.data.historical import StockHistoricalDataClient #, StockLatestTradeRequest
from alpaca.trading.client import TradingClient , GetAssetsRequest
from alpaca.trading.enums import AssetStatus, ContractType, OrderSide, OrderType, TimeInForce, QueryOrderStatus


load_dotenv()
trade_client = TradingClient(api_key=os.getenv("api_key"),secret_key=os.getenv("secret_key"), paper=True)
stock_data_client = StockHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))
option_data_client = OptionHistoricalDataClient(api_key=os.getenv("api_key"), secret_key=os.getenv("secret_key"))

acct = trade_client.get_account()
print(f"Options approved level: {acct.options_approved_level}")
print(f"Option trading level: {acct.options_trading_level}")
print(f"Option buying power: {acct.options_buying_power}")

# set the account configuration 
acct_config = trade_client.get_account_configurations()
print(f"Max options approved level: {acct_config.max_options_trading_level}")

acct_config.max_options_trading_level = 3
trade_client.set_account_configurations(acct_config)

acct_config = trade_client.get_account_configurations()
print(f"Max options approved level: {acct_config.max_options_trading_level}")


# assets
req = GetAssetsRequest(
    status = AssetStatus.ACTIVE,
    attributes = "options_enabled",
)

options_enabled_underlyings = trade_client.get_all_assets(req)
print(f"Num of underlyings with options: {len(options_enabled_underlyings)}")