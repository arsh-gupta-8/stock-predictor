from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def testModel(data, model):

  xTest = data.drop(columns=['Target', 'Date'])
  yTest = data['Target']

  yPrediction = model.predict(xTest)
  print(f"MSE: {mean_squared_error(yTest, yPrediction):.4f}")
  print(f"R2: {r2_score(yTest, yPrediction):.4f}")
  print(f"Direction Predicted: {((np.sum(np.sign(yPrediction) == np.sign(yTest))) / len(yPrediction)):.4f}")