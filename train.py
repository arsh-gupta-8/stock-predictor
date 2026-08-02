import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def makeModel(data):

  x = data.drop(columns=['Target'])
  y = data['Target']

  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit()