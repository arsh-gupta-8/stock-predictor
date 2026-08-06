import pickle

def saveModel(model, modelName="MODEL"):
  with open(f'{modelName}_model.pkl', 'wb') as file:
    pickle.dump(model, file)

def loadModel(modelName="MODEL"):
  with open(f'{modelName}_model.pkl', 'rb') as file:
    return pickle.load(file)
