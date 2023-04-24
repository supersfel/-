import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


df = pd.read_csv('./Cancer_Data.csv')
# df = df.dropna(axis=0)
df.info()
Y = df[['diagnosis']].to_numpy()

X = df.drop(columns=['diagnosis','id','Unnamed: 32']).to_numpy()



import matplotlib.pyplot as plt

pltY = Y.reshape(-1)
pltX1 = [ x[1] for x in X]
pltX2 = [ x[2] for x in X]

pltX1_true,pltX1_false,pltX2_true,pltX2_false = [],[],[],[]

for i in range(569):
  if pltY[i]=='B':
    pltX1_true.append(pltX1[i])
    pltX2_true.append(pltX2[i])
  else:
    pltX1_false.append(pltX1[i])
    pltX2_false.append(pltX2[i])

plt.scatter(pltX1_true,pltX2_true,c='c')
plt.scatter(pltX1_false,pltX2_false,c='g')
plt.show()


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.1,random_state=2023)




model1 = DecisionTreeClassifier()
model1.fit(X_train,Y_train)
print(model1.score(X_test,Y_test))
