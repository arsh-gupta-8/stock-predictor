import pandas as pd
import test

def backtest(model, testingData, startAmount=10000):

  pred = test.givePrediction(data=testingData, model=model)
  actualReturn = testingData["Return1"].reset_index(drop=True)

  wallet = startAmount
  inShares = False
  shareValue = 0

  for i in range(len(pred)):
    todayActualReturn = actualReturn[i]

    if not inShares:
      if pred[i] > 0.005:
        inShares = True
        shareValue = wallet
        wallet = 0
            
    else:
      shareValue = shareValue * (1 + todayActualReturn)

      if todayActualReturn <= -0.01 or pred[i] < -0.005:
        wallet = shareValue
        shareValue = 0
        inShares = False


  finalMoney = wallet if not inShares else shareValue
  
  print(f"Final Wallet: ${finalMoney:.2f}")
  print(f"Total Return: {((finalMoney / startAmount) * 100):.2f}%")

  return finalMoney
  

