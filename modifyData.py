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