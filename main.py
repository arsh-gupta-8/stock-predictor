import yfinance as yf
import pandas as pd
import features as md
import train
import test
import save as sl
import backtesting as bt
import paperTrade



def getStockData(stockName):
  trainingFile = f"Data/{stockName}-train.csv"
  testingFile = f"Data/{stockName}-test.csv"

  stockDataFrame = yf.download(stockName, start="2005-7-31", end="2025-7-31", interval="1d").reset_index()

  if stockDataFrame.empty:
    return 0

  stockDataFrame.to_csv(trainingFile, index=False)

  stockDataFrame = yf.download(stockName, start="2025-8-1", interval="1d").reset_index()
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



def addFeaturesCombine(stockNames, use="train"):

  finalData = None

  for index, stock in enumerate(stockNames):
    data = md.featureEngineer(data=pd.read_csv(f"Data/{stock}-{use}.csv"), recordsUsed=RECORD_MARGIN, use=use)
    if index == 0:
      finalData = data
    else:
      finalData = pd.concat([finalData, data], ignore_index=True)

  return finalData



def getTodayStockData(stockName):
  getStockData(stockName=stockName)
  return addFeaturesCombine(stockNames=[stockName], use="test").iloc[[-1]]



def main():

  stockModel = None
  stockNamesTraining = ["AAPL", "MSFT", "NVDA", "JPM", "BAC", "AMZN", "WMT", "JNJ", "PFE", "SPY"]
  stockNamesTesting = ["SPY"]
  stockNamesTrading = ["AAPL", "MSFT", "NVDA", "JPM", "BAC", "AMZN", "WMT", "JNJ", "PFE", "SPY"]

  option = -1
  while option != 9:
    option = int(input("""Would you like to 
    (0) Access Alpaca for paper trading
    (1) Edit training stocks 
    (2) Edit testing stocks
    (3) Train and save a new model
    (4) Load an existing model
    (5) Look at model stastics 
    (6) Backtest a model
    (9) Exit
    ::: """))

    print()

    if option == 0:
      stockDataToday = [getTodayStockData(stockName=stockName) for stockName in stockNamesTrading]
      paperTrade.makeTrade(stockNames=stockNamesTrading, allStockToday=stockDataToday, model=stockModel)

    elif option == 1:

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

    elif option == 2:
    
        while True:
          print(stockNamesTesting)
          stockEdit = input("Enter name of stock to add/remove or EXIT ::: ").upper()
          if stockEdit == "EXIT":
            break
          else:
            if stockEdit in stockNamesTesting:
              stockNamesTesting.remove(stockEdit)
            else:
              stockNamesTesting.append(stockEdit)
    
    elif option == 3:

      modelName = input("What would you like to name this model ::: ")

      stockNamesTraining = checkStockData(stockNames=stockNamesTraining)
      trainingData = addFeaturesCombine(stockNames=stockNamesTraining, use="train")

      print("Data is ready. Training model ...")
      stockModel = train.trainModel(data=trainingData)
      sl.saveModel(model=stockModel, modelName=modelName)


    elif option == 4:

      modelName = input("What is the name of the model ::: ")

      try:
        stockModel = sl.loadModel(modelName=modelName)
        print("Model selected successfuly")
      except:
        print("Model doesn't exist")

    elif option == 5:
      if stockModel == None:
        print("No model selected")
      else:
        stockNamesTesting = checkStockData(stockNames=stockNamesTesting)
        testingData = addFeaturesCombine(stockNames=stockNamesTesting, use="test")

        test.testModel(data=testingData, model=stockModel)

    elif option == 6:
      stockNamesTesting = checkStockData(stockNames=stockNamesTesting)
      total = 0

      for stockName in stockNamesTesting:
        testingData = addFeaturesCombine(stockNames=[stockName], use="test")
        startAmount = int(input(f"Choose a starting amount for stock {stockName} ::: "))
        total += bt.backtest(model=stockModel, testingData=testingData, startAmount=startAmount)

      print("Total for all Stocks: " + total)


    if option != 9:
      print()
      input("Press ENTER to Continue ::: ")
      print()



RECORD_MARGIN = 20
main()