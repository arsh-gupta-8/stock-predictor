import yfinance as yf
import pandas as pd
import modifyData as md

# stockDataFrame = yf.download("AAPL", period="1y", interval="1d").reset_index()
# stockDataFrame.to_csv('output.csv', index=False)

RECORD_MARGIN = 20

filename = "output.csv"
data = pd.read_csv(filename)
data = md.removeTopLine(data=data)
data = md.featureEngineer(data=data, recordsUsed=RECORD_MARGIN)
# data['SMA20'] = data['Close'].rolling(window=20).mean()

print(data)