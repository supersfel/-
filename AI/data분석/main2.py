import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('시군구_인구동태건수_및_동태율_출생_사망_혼인_이혼__20230225113457.csv',encoding='cp949')
# print(df)

df = df.T
print(df)

df.columns = df.iloc[0].to_numpy()
df = df.drop('행정구역별')
print(df)