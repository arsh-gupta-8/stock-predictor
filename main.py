import yfinance as yf
import pandas as pd
import features as md
import sklearn as sk

trainingFile = "Data/AAPL-train.csv"
testingFile = "Data/AAPL-test.csv"

stockDataFrame = yf.download("AAPL", start="2005-7-31", end="2025-7-31", interval="1d").reset_index()
stockDataFrame.to_csv(trainingFile, index=False)

stockDataFrame = yf.download("AAPL", start="2025-8-1", end="2026-8-1", interval="1d").reset_index()
stockDataFrame.to_csv(testingFile, index=False)

RECORD_MARGIN = 20

data = pd.read_csv(trainingFile)
# data = md.removeTopLine(data=data)
# data = md.featureEngineer(data=data, recordsUsed=RECORD_MARGIN)
# # data['SMA20'] = data['Close'].rolling(window=20).mean()

# print(data)

print(data)