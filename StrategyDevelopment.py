import pandas as pd
#import pandas_ta as ta
from backtesting import Backtest, Strategy
import optuna


## GETTING / FORMATTING DATASET
df = pd.read_csv('crypto_data_latest.csv')
df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
df.drop(columns=["vwap", "trade_count","symbol"], inplace=True)

#df["Date"] = pd.to_datetime(df["Date"])
#df.set_index("Date", inplace=True)
print(df.head())
df.dropna(inplace=True)


# INDICATORS
def UpperBollingerBand(price, period=20, std_dev=2):
    ma = pd.Series(price).rolling(window=period).mean()
    std = pd.Series(price).rolling(window=period).std()
    return ma + (std_dev * std)

def LowerBollingerBand(price, period=20, std_dev=2):
    ma = pd.Series(price).rolling(window=period).mean()
    std = pd.Series(price).rolling(window=period).std()
    return ma - (std_dev * std)

def MovingAverage(price,period):
    return pd.Series(price).rolling(window=period).mean()

def ExponentialMovingAverage(price, period):
    return pd.Series(price).ewm(span=period, adjust=False).mean()

def RelativeStrengthIndex(price, period=14):
    delta = pd.Series(price).diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# STRATEGIES
class SMACross(Strategy):
    n_short = 10
    n_long = 50

    def init(self):
        #close = self.data.Close
        self.ma_short = self.I(ExponentialMovingAverage, self.data.Close, self.n_short)
        self.ma_long = self.I(ExponentialMovingAverage, self.data.Close, self.n_long)

    def next(self):
        if self.ma_short[-2] < self.ma_long[-2]:
            if self.ma_short[-1] > self.ma_long[-1]:
                self.buy()

        elif self.ma_short[-2]  >  self.ma_long[-2]:
            if self.ma_short[-1]  <  self.ma_long[-1]:
                if self.position:
                    self.position.close()

class RSI(Strategy):
    n = 7

    def init(self):
        self.rsi = self.I(RelativeStrengthIndex, self.data.Close, self.n)

    def next(self):
        if self.rsi[-1] < 30:
            if not self.position:
                self.buy()

        elif self.rsi[-1] > 70:
            if self.position:
                self.position.close()

class BB(Strategy): 
    n = 20

    def init(self):
        self.UB = self.I(UpperBollingerBand, self.data.Close, self.n)
        self.LB = self.I(LowerBollingerBand, self.data.Close, self.n)

    def next(self):
        if self.data.Close[-1]  > self.UB[-1]:
            if not self.position:
                self.buy()

        elif self.data.Close[-1] < self.LB[-1]:
            if self.position:
                self.position.close()

#OPTIMIZATION objectives
def objective(trial):
    n_short = trial.suggest_int('n_short', 5, 60)
    n_long = trial.suggest_int('n_long', n_short+1, 480)

    bt = Backtest(df, SMACross, cash=1000000000, commission=0)
    output = bt.run(n_short=n_short, n_long=n_long)
    return output['Return [%]']


# OPTIMIZATION Start
study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective, n_trials=10)
print("Best parameters:", study.best_params)