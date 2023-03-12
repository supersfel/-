import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('train.csv')
print(df)
print(df['Survived'].value_counts())

df['Survived'] = df['Survived'].replace(0,'Perish')
df['Survived'] = df['Survived'].replace(1,'Survived')

print(df)


df['Pclass'] = df['Pclass'].replace(1,'1st')
df['Pclass'] = df['Pclass'].replace(2,'2nd')
df['Pclass'] = df['Pclass'].replace(3,'3rd')

print(df)

sns.countplot(data = df,x='Survived',hue = 'Pclass')
plt.show()