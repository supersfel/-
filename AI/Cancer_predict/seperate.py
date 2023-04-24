import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


df = pd.read_csv('./Cancer_Data.csv')
# df = df.dropna(axis=0)
df.info()
Y = df[['diagnosis']]

X = df.drop(columns=['diagnosis','id','Unnamed: 32']).to_numpy()