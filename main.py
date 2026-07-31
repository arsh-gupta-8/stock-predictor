import yfinance as yf
import pandas as pd
import modifyData as md

# stockDataFrame = yf.download("AAPL", period="1y", interval="1d").reset_index()
# stockDataFrame.to_csv('output.csv', index=False)

filename = "output.csv"
SMA_margin = 20

data = md.removeTopLine(filename=filename)
data = md.featureEngineer(data=data, recordsUsed=SMA_margin)
# data['SMA20'] = data['Close'].rolling(window=20).mean()

print(data)