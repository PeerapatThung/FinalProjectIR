import pandas as pd

dataset = pd.read_csv('ingredient_dataset.csv')
dataset = dataset.drop(['Unnamed: 0', 'Ingredients'],axis=1)