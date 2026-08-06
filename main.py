import yfinance as yf
import pandas as pd
import features as md
import train
import test
import save as sl
import backtesting as bt

def getStockData(stockName):
  trainingFile = f"Data/{stockName}-train.csv"
  testingFile = f"Data/{stockName}-test.csv"

  stockDataFrame = yf.download(stockName, start="2005-7-31", end="2025-7-31", interval="1d").reset_index()

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


def addFeaturesCombine(stockNamesTraining, stockNamesTesting):

  finalTrainingData = None

  for index, stock in enumerate(stockNamesTraining):
    trainingData = md.featureEngineer(data=pd.read_csv(f"Data/{stock}-train.csv"), recordsUsed=RECORD_MARGIN)
    if index == 0:
      finalTrainingData = trainingData
    else:
      finalTrainingData = pd.concat([finalTrainingData, trainingData], ignore_index=True)

  finalTestingData = None

  for index, stock in enumerate(stockNamesTesting):
    testingData = md.featureEngineer(data=pd.read_csv(f"Data/{stock}-test.csv"), recordsUsed=RECORD_MARGIN)
    if index == 0:
      finalTestingData = testingData
    else:
      finalTestingData = pd.concat([finalTestingData, testingData], ignore_index=True)
  
  return finalTrainingData, finalTestingData


def main():

  stockModel = None
  stockNamesTraining = ["AAPL", "MSFT"]
  stockNamesTesting = ["GOOGL"]

  option = int(input("""Would you like to 
  (1) Edit training stocks 
  (2) Edit testing stocks
  (3) Train and save a new model
  (4) Load an existing model
  (5) Look at model stastics 
  (6) Backtest a model
  ::: """))

  stockNamesTraining = checkStockData(stockNames=stockNamesTraining)
  stockNamesTesting = checkStockData(stockNames=stockNamesTesting)
  trainingData, testingData = addFeaturesCombine(stockNamesTraining=stockNamesTraining, stockNamesTesting=stockNamesTesting)

  if option == 1:

    while True:
      print(stockNamesTraining)
      stockEdit = input("Enter name of stock to add/remove or EXIT ::: ").upper()
      if stockEdit == "EXIT":
        break
      else:
        if stockEdit in stockNamesTraining:
          stockNamesTraining.remove(stockEdit)
        else:
          stockNamesTraining.append(stockEdit)


  elif option == 3:
    modelName = input("What would you like to name this model ::: ")

    stockModel = train.trainModel(data=trainingData)
    sl.saveModel(model=stockModel, modelName=modelName)

  elif option == 4:
    modelName = input("What is the name of the model ::: ")

    stockModel = sl.loadModel(modelName=modelName)

  # elif option == 6:
  #   startAmount = int(input("Choose a starting amount ::: "))
  #   bt.backtest(model=stockModel, testingData=testingData, startAmount=startAmount)


RECORD_MARGIN = 20

# predictions = test.testModel(data=testingData, model=stockModel)

main()