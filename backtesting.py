import pandas as pd

def backtest(model, testingData):
  test = testingData.drop(columns=['Target', 'Date'], errors='ignore')
  pred = model.predict(test)

  actualReturn = testingData["Return1"].reset_index(drop=True)

  startValue = 100000
  wallet = 100000
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


  final_wallet = wallet if not inShares else shareValue
  
  total_return_pct = (final_wallet / startValue) * 100
  print(f"Final Wallet: ${final_wallet:.2f} | Total Return: {total_return_pct:.2f}%")
  

