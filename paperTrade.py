from dotenv import load_dotenv
from Strategies import DailyBuySellCheck as dbsc
import os
import test
import json
import time

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

def makeTrade(stockNames, allStockToday, model):
  API_key = os.getenv("ALPACA_API_KEY")
  SECRET_key = os.getenv("ALPACA_SECRET_KEY")

  tradeClient = TradingClient(API_key, SECRET_key, paper=True)
  stockStatus = {}

  with open("stockStatus.json", "r+") as file:
    data = json.load(file)

    for stock in stockNames:
      if stock not in data:
        data[stock] = False
        data[stock+"Value"] = 10000

    stockStatus = data.copy()

    file.seek(0)
    file.truncate()

    json.dump(data, file, indent=4)

  for i in range(len(stockNames)):
    prediction = test.givePrediction(data=allStockToday[i], model=model)
    decision = dbsc.stockDecision(pred=prediction, todayReturn=allStockToday[i]["Return1"], inShares=stockStatus[stockNames[i]])

    if decision == "BUY":
      buyRequest = MarketOrderRequest(
        symbol=stockNames[i],
        notional=stockStatus[stockNames[i]+"Value"],
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
      )

      buyOrder = tradeClient.submit_order(order_data=buyRequest)
      print(f"Invested ${stockStatus[stockNames[i]+"Value"]} into {stockStatus[stockNames[i]+"Value"]}. Order ID: {buyOrder.id}")

      stockStatus[stockNames[i]] = True

    elif decision == "SELL":
      try:
        cashBefore = float(tradeClient.get_account().cash)
        tradeClient.close_position(stockNames[i])
        time.sleep(3) 
        cashAfter = float(tradeClient.get_account().cash)
        deltaCash = cashAfter - cashBefore
        print(f"Successfully sold all shares of {stockNames[i]} for ${deltaCash}")
        stockStatus[stockNames[i]+"Values"] = deltaCash
      except Exception as e:
        print(f"Could not sell. Ensure you actually hold a position: {e}")

  with open("stockStatus.json", "w") as file:
    json.dump(stockStatus, file, indent=4)
