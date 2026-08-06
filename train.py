import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def trainModel(data):

  xTrain = data.drop(columns=['Target', 'Date'])
  yTrain = data['Target']

  model = RandomForestRegressor(n_estimators=500)
  model.fit(xTrain, yTrain, random_state=42)

  return model