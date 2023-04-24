
import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv('./Cancer_Data.csv')
# df = df.dropna(axis=0)
# df.info()
# Y = df[['diagnosis']]
#
# X = df.drop(columns=['diagnosis','id','Unnamed: 32']).to_numpy()
train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)

train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)