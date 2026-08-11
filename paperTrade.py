from dotenv import load_dotenv
import Strategies as strat
import os
import test
import json
import time
import math
import numpy as np

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()


def stockAction(decision, stockStatus, stockName, tradeClient, buyAmount=0):
  if decision == "BUY":
    buyRequest = MarketOrderRequest(
      symbol=stockName,
      notional=buyAmount,
      side=OrderSide.BUY,
      time_in_force=TimeInForce.DAY
    )

    with open("stockHistory.txt", "a") as history:
      history.write(f"\nBUY {stockName} FOR ${buyAmount}")

    buyOrder = tradeClient.submit_order(order_data=buyRequest)
    print(f"Invested ${buyAmount} into {stockName}. Order ID: {buyOrder.id}")

    stockStatus[stockName]["inShares"] = True
    stockStatus[stockName]["buyValue"] = buyAmount

  elif decision == "SELL":
    try:

      positionOrder = tradeClient.close_position(stockName)
      orderID = positionOrder.id
      deltaCash = 0
      max_retries = 10
      for _ in range(max_retries):
        orderStatus = tradeClient.get_order_by_id(orderID)
        if orderStatus.status == 'filled':
          filledQuantity = float(orderStatus.filled_qty)
          avgPrice = float(orderStatus.filled_avg_price)
          
          deltaCash = filledQuantity * avgPrice
          break
        time.sleep(1)

      deltaCashPCT = ((deltaCash - stockStatus[stockName]["buyValue"]) / stockStatus[stockName]["buyValue"]) * 100
      print(f"Successfully sold all shares of {stockName} for ${deltaCash} giving return of {(deltaCashPCT):.4f}%")

      stockStatus[stockName]["buyValue"] = 0
      stockStatus[stockName]["inShares"] = False

      with open("stockHistory.txt", "a") as history:
        history.write(f"\nSOLD {stockName} FOR ${deltaCash} AND RETURN {(deltaCashPCT):.4f}%")

    except Exception as e:
      print(f"Could not sell. Ensure you actually hold a position: {e}")

  return stockStatus


def makeTrade(stockNames, allStockToday, model, viewMode=False):
  API_key = os.getenv("ALPACA_API_KEY")
  SECRET_key = os.getenv("ALPACA_SECRET_KEY")

  tradeClient = TradingClient(API_key, SECRET_key, paper=True)
  account = tradeClient.get_account()
  stockStatus = {}
  
  with open("stockStatus.json", "r+") as file:
    data = json.load(file)

    for stock in stockNames:
      if stock not in data:
        data[stock] = {}
        data[stock]["inShares"] = False
        data[stock]["buyValue"] = 0

    stockStatus = data.copy()

    file.seek(0)
    file.truncate()

    json.dump(data, file, indent=4)

  predictions = test.givePrediction(data=allStockToday, model=model)
  stockNamesNP = np.array(stockNames)

  sortOrder = np.argsort(predictions)

  predictions = predictions[sortOrder][::-1]
  stockNamesNP = stockNamesNP[sortOrder][::-1]

  
  for i in range(len(stockNames)):
    print(f"{i+1}. {stockNamesNP[i]}")
    print(f"This stock is expected to change by {(predictions[i] * 100):.4f}%")

  if not viewMode:
    print("\nNow accessing API for trading\n")

    print("---------- NOW SELLING ----------")

    for i in range(len(stockNames)):
      if stockStatus[stockNamesNP[i]]["inShares"]:
        print(f"{i+1}. For the stock {stockNamesNP[i]}")
        accountShare = tradeClient.get_open_position(stockNamesNP[i])
        currentAmount = float(accountShare.market_value)
        valueChange = (currentAmount - stockStatus[stockNamesNP[i]]["buyValue"]) / stockStatus[stockNamesNP[i]]["buyValue"]
        decision = strat.DayBuySellCheck(pred=predictions[i], inShares=stockStatus[stockNamesNP[i]]["inShares"], valueChange=valueChange)
        if decision == "SELL":
          stockStatus = stockAction(decision=decision, stockStatus=stockStatus, stockName=stockNamesNP[i], tradeClient=tradeClient)

    print("Please wait while any sell transactions are pending")
    time.sleep(10) # TIME FOR ALPACA TO PROCESS ANY SELL TRANSACTIONS
    inShareCount = 0

    for stock in stockNames:
      if data[stock]["inShares"]:
        inShareCount += 1

    canBuy = 10 - inShareCount
    cashPerStock = math.floor(float(account.non_marginable_buying_power) / canBuy)

    print("---------- NOW BUYING ----------")

    for i in range(len(stockNames)):
      if not stockStatus[stockNamesNP[i]]["inShares"]:
        print(f"{i+1}. For the stock {stockNamesNP[i]}")
        if canBuy > 0:
          decision = strat.DayBuySellCheck(pred=predictions[i], inShares=stockStatus[stockNamesNP[i]]["inShares"])
          if decision == "BUY":
            stockStatus = stockAction(decision=decision, stockStatus=stockStatus, stockName=stockNamesNP[i], tradeClient=tradeClient, buyAmount=cashPerStock)
            canBuy -= 1
        else:
          print("Change lower than others so IGNORED")
        

  with open("stockStatus.json", "w") as file:
    json.dump(stockStatus, file, indent=4)
