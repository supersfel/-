import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('시군구_인구동태건수_및_동태율_출생_사망_혼인_이혼__20230225113457.csv',encoding='cp949')



df = df.T
df.columns = df.iloc[0].to_numpy()
df = df.drop('행정구역별')
print(df)

출생수 = df[df['행정구역별'] == '출생건수 (명)']
print(출생수)
출생수 = 출생수[['전국']].to_numpy(dtype='int')
print(출생수)

사망수 = df[df['행정구역별'] == '사망건수 (명)']
사망수 = 사망수[['전국']].to_numpy(dtype='int')

plt.plot(list(range(2000,2022)),사망수, label="death")
plt.plot(list(range(2000,2022)),출생수,label = 'birth')

plt.legend()
plt.show()
