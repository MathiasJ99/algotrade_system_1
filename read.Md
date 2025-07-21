# explanation
trade system made up of 3 files
- GetMartekData
- StrategyDevelopment
- TradeStream


# GetMarketData
this gets market data for last 3 weeks, saves to csv
output -  csv file called crypto_data_latest

# StrategyDevelopment - todo
this will take csv and uses it to backtest strategies, should generate optimial entry and exit points along with strats
inputs - csv file
output - entry price, exit price and strat

# TradeSystem - todo
this will monitor current prices and execute trades if conditions met
inputs - entry price, exit price and strat
output - saves log of each trade to db
