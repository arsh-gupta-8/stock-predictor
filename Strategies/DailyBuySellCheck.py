import test
import yfinance as yf

def stockDecision(pred, todayReturn, inShares):

  if not inShares:
    if pred > 0.005:
      print(f"Expected to increase by {pred * 100}% so BUYING")
      return "BUY"
          
  elif todayReturn <= -0.01 or pred < -0.005:
    print(f"Expected to decrease by {pred * 100}% so SELLING")
    return "SELL"

  print("No Major Changes so HOLDING")
  return "HOLD"
  
  
