import pandas as pd
import numpy as np


def removeTopLine(data):
  return data.iloc[1:]


def featureEngineer(data, recordsUsed=20):

  # Convert all columns to appropriate datatypes first
  data['Close'] = data['Close'].astype(float)
  data['High'] = data['High'].astype(float)
  data['Low'] = data['Low'].astype(float)
  data['Open'] = data['Open'].astype(float)
  data['Volume'] = data['Volume'].astype(int)

  # Simple Moving Average
  data['SMA20'] = data['Close'].rolling(window=recordsUsed).mean()

  # Exponentially Moving Average
  data = EMA_calc(data, recordsUsed=recordsUsed)

  # List Close price against average
  data['Price_vs_SMA20'] = data['Close'] / data['SMA20']

  # 1 Day % Change
  data['Return1'] = data['Close'].pct_change().fillna(0)

  # 5 Day % Change
  data['Return5'] = data['Close'].pct_change(periods=5).fillna(0)

  # 6 Relative Strength Index
  data = RSI(data)

  # 7 Volume Ratio
  data['volRatio'] = data['Volume'] / data['Volume'].rolling(window=recordsUsed).mean()

  # 8 Volatility
  data['Volatility20'] = data['Return1'].rolling(window=recordsUsed).std()

  # 9 Lag1
  data["Lag1"] = data["Return1"].shift(1)

  # 10 Lag2
  data["Lag2"] = data["Return1"].shift(2)

  # TARGET
  data["Target"] = data["Return1"].shift(-1)

  return data


def EMA_calc(data, recordsUsed):

  # Custom Written Code Function
  # ema_values = np.full(len(data), np.nan)
  # ema_values[recordsUsed-1] = data['SMA20'].iloc[recordsUsed-1]
  # close_values = data['Close']

  # for i in range(len(data) - recordsUsed):
  #   recordNum = recordsUsed + i
  #   aVal = 2/(recordsUsed + 1)
  #   ema_values[recordNum] = (aVal * close_values[recordNum]) + ((1 - aVal) * ema_values[recordNum - 1])

  # data['EMA20'] = ema_values

  # Pre Built Code Function
  data['EMA20'] = data['Close'].ewm(span=recordsUsed, adjust=False).mean()

  return data


def RSI(data, window=14):

  RSI_values = np.full(len(data), np.nan)

  delta = data['Close'].diff()

  for record in range(window + 1, len(data) + 1):
    gains, losses = 0, 0
    for diff in delta[record-window+1:record+1]:
      if diff >= 0:
        gains += diff
      else:
        losses -= diff

    gain_avg = gains / 14
    loss_avg = losses / 14
    rs = gain_avg / loss_avg

    RSI_values[record - 1] = 100 - (100 / (1 + rs))

  data['RSI'] = RSI_values

  return data