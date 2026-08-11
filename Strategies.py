import test
import yfinance as yf

def DayBuySellCheck(pred, inShares, valueChange):

  if not inShares:
    if pred > 0.005:
      print(f"Expected to increase by {pred * 100}% so BUYING")
      return "BUY"
          
  elif (valueChange < -0.01 and pred < 0.005) or pred < -0.005:
    print(f"Expected to decrease by {pred * 100}% so SELLING")
    return "SELL"

  print("No Major Changes so HOLDING")
  return "HOLD"
  
  
