import test
import yfinance as yf

def DayBuySellCheck(pred, inShares, valueChange=0):

  if not inShares:
    if pred > 0.005:
      print(f"Expected to increase by {pred * 100}% so BUYING")
      return "BUY"
    else:
      print(f"Expected to change by {pred * 100}% so NOT BUYING")
          
  else:
    if (valueChange < -0.01 and pred < 0.005) or pred < 0:
      print(f"Expected to decrease by {pred * 100}% so SELLING")
      return "SELL"
    else:
      print(f"Expected to change by {pred * 100}% so HOLDING")
  
  return "HOLD"
  
  
