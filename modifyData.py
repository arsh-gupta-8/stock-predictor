import pandas as pd

def removeTopLine(filename):
  try:
    return pd.read_csv(filename).iloc[1:]
  except FileNotFoundError:
    print("File was not found")

def featureEngineer(data, recordsUsed=20):
  data['SMA20'] = data['Close'].rolling(window=recordsUsed).mean()
  return data