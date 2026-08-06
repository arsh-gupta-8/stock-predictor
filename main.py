import yfinance as yf
import pandas as pd
import features as md
import train
import test
import save as sl


def getStockData(stockName):
  trainingFile = f"Data/{stockName}-train.csv"
  testingFile = f"Data/{stockName}-test.csv"

  stockDataFrame = yf.download(stockName, start="2005-7-31", end="2025-7-31", interval="1d").reset_index()

  print(stockDataFrame)
  print(stockDataFrame.empty)
  if stockDataFrame.empty:
    return 0

  stockDataFrame.to_csv(trainingFile, index=False)

  stockDataFrame = yf.download(stockName, start="2025-8-1", end="2026-8-1", interval="1d").reset_index()
  stockDataFrame.to_csv(testingFile, index=False)

  return 1
  

def checkStockData(stockNames):
  for stock in stockNames[:]:
    try:
      trainingData = pd.read_csv(f"Data/{stock}-train.csv")
    except(FileNotFoundError):
      Added = getStockData(stock)
      if not Added:
        stockNames.remove(stock)

  return stockNames


def addFeaturesCombine(stockNames):
  finalTrainingData = None
  finalTestingData = None
  for index, stock in enumerate(stockNames):
    trainingData = md.featureEngineer(data=pd.read_csv(f"Data/{stock}-train.csv"), recordsUsed=RECORD_MARGIN)
    testingData = md.featureEngineer(data=pd.read_csv(f"Data/{stock}-test.csv"), recordsUsed=RECORD_MARGIN)
    if index == 0:
      finalTrainingData = trainingData
      finalTestingData = testingData
    else:
      finalTrainingData = pd.concat([finalTrainingData, trainingData], ignore_index=True)
      finalTestingData = pd.concat([finalTestingData, testingData], ignore_index=True)
  return finalTrainingData, finalTestingData
  

RECORD_MARGIN = 20
stockNames = ["AAPL", "MSFT"]
stockNames = checkStockData(stockNames=stockNames)
trainingData, testingData = addFeaturesCombine(stockNames=stockNames)

# CREATE AND SAVE MODEL
# stockModel = train.trainModel(data=trainingData)
# sl.saveModel(model=stockModel, modelName="RFR")

# LOAD MODEL
stockModel = sl.loadModel(modelName="RFR")

predictions = test.testModel(data=testingData, model=stockModel)