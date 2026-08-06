import test
import yfinance as yf

def stockDecision(pred, todayReturn, inShares):

  if not inShares:
    if pred > 0.005:
      return "BUY"
          
  elif todayReturn <= -0.01 or pred < -0.005:
    return "SELL"

  return "HOLD"
  
  
