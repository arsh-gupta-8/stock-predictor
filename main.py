import yfinance as yf
import pandas as pd
import features as md
import train
import test


def getStockData(stockName):
  trainingFile = f"Data/{stockName}-train.csv"
  testingFile = f"Data/{stockName}-test.csv"

  stockDataFrame = yf.download(stockName, start="2005-7-31", end="2025-7-31", interval="1d").reset_index()
  stockDataFrame.to_csv(trainingFile, index=False)

  stockDataFrame = yf.download(stockName, start="2025-8-1", end="2026-8-1", interval="1d").reset_index()
  stockDataFrame.to_csv(testingFile, index=False)


RECORD_MARGIN = 20
STOCK = "AAPL"

# getStockData(STOCK)

trainingData = pd.read_csv(f"Data/{STOCK}-train.csv")
testingData = pd.read_csv(f"Data/{STOCK}-test.csv")

trainingData = md.featureEngineer(data=trainingData, recordsUsed=RECORD_MARGIN)
testingData = md.featureEngineer(data=testingData, recordsUsed=RECORD_MARGIN)

stockModel = train.trainModel(data=trainingData)
predictions = test.testModel(data=testingData, model=stockModel)

# print(trainingData)