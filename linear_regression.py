# -*- coding: utf-8 -*-
"""Linear Regression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16BZ9N3ewBz6c5BfCZTCf5Hcuj2hoOC4g

#1) To load libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

"""#2) To load data and check"""

Atrain = pd.read_csv('A-train.csv')

Btrain = pd.read_csv('B-train.csv')

Atest = pd.read_csv('A-test.csv')

Btest = pd.read_csv('B-test.csv')

Atrain

Btrain

Atest

Btest

Atrain.info()

Btrain.info()

Atrain.describe()

Btrain.describe()

"""#3) Data exploration

##3.1) Data processing

###3.1.1)Missing Values
"""

Atrain = Atrain.fillna(Atrain.mean())

Btrain = Btrain.fillna(Btrain.mean())

Atest = Atest[["x8","x3"]]

Btest = Btest[["x1","x2"]]

Atest = Atest.fillna(Atest.mean())

Btest = Btest.fillna(Btest.mean())

Atrain.info()

Btrain.info()

Atest.info()

Btest.info()

"""###3.1.2) outlier"""

def plot_boxplot(df,ft):
  df.boxplot(column=[ft])
  plt.grid(False)
  plt.show()

plot_boxplot(Atrain,"x8")

plot_boxplot(Btrain,"x1")

def outliers(df,ft):
    Q1 = df[ft].quantile(0.25)
    Q3 = df[ft].quantile(0.75)
    IQR = Q3 - Q1

    upper_bound = Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR

    ls = df.index[(df[ft] < lower_bound) | (df[ft] > upper_bound)]
    return ls

index_listA = []
for feature in ['x1','x2','x3','x4','x5','x6','x7','x8']:
    index_listA.extend(outliers(Atrain,feature))

index_listB = []
for feature in ['x1','x2','x3','x4','x5','x6','x7','x8']:
    index_listB.extend(outliers(Btrain,feature))

index_listA

index_listB

def remove(df,ls):
  ls = sorted(set(ls))
  df = df.drop(ls)
  return df

new_Atrain = remove(Atrain,index_listA)

new_Btrain = remove(Btrain,index_listB)

new_Atrain.info()

new_Btrain.info()

new_Atrain.shape

new_Btrain.shape

"""#4) data exploration"""

sns.pairplot(new_Atrain, x_vars=new_Atrain.columns, y_vars=["y"])

sns.pairplot(new_Btrain, x_vars=new_Btrain.columns, y_vars=["y"])

sns.displot(new_Atrain['y'])

sns.displot(new_Btrain['y'])

"""##4.1) to check the correlation"""

new_Atrain.corr()

new_Btrain.corr()

sns,sns.heatmap(new_Atrain.corr())

sns,sns.heatmap(new_Btrain.corr())

new_Atrain.corr().sort_values('y')[['y']]

new_Btrain.corr().sort_values('y')[['y']]

sns.pairplot(new_Atrain, x_vars=["x8","x3"], y_vars=["y"])

sns.pairplot(new_Btrain, x_vars=["x1","x2"], y_vars=["y"])

"""##4.2) to select data"""

X_A= new_Atrain[["x8","x3"]]
y_A = new_Atrain["y"]

X_B= new_Btrain[["x1","x2"]]
y_B= new_Btrain["y"]

X_A

y_A

X_B

y_B

"""#5) To create a Linear Regression Model

##5.1) to split train and test datasets
"""

X_train_A, X_test_A, y_train_A, y_test_A = train_test_split(X_A,y_A,test_size=0.3,random_state=101)

X_train_B, X_test_B, y_train_B, y_test_B = train_test_split(X_B,y_B,test_size=0.3,random_state=101)

print("len(X_train) : ", len(X_train_A))
print("len(X_test) : ", len(X_test_A))
print("len(y_train) : ", len(y_train_A))
print("len(y_test) : ", len(y_test_A))

print("len(X_train) : ", len(X_train_B))
print("len(X_test) : ", len(X_test_B))
print("len(y_train) : ", len(y_train_B))
print("len(y_test) : ", len(y_test_B))

"""##5.2) to train and create a linear regression model"""

lmA = LinearRegression()

lmB = LinearRegression()

lmA.fit(X_train_A,y_train_A)

lmB.fit(X_train_B,y_train_B)

lmA.coef_

lmB.coef_

lmA.intercept_

lmB.intercept_

print("LM MODEL")
print("")
print(y_A.name, "=")
for i in range(0,len(X_A.columns)):
  print("", lmA.coef_[i],"*",X_A.columns[i],"   +")
print("", lmA.intercept_)

print("LM MODEL")
print("")
print(y_B.name, "=")
for i in range(0,len(X_B.columns)):
  print("", lmB.coef_[i],"*",X_B.columns[i],"   +")
print("", lmB.intercept_)

"""#6) To evaluate the model

##6.1) to predict from the test set
"""

y_pred_A = lmA.predict(X_test_A)

#y_pred_A = lmA.predict(Atest)

y_pred_B = lmB.predict(X_test_B)

#y_pred_B = lmB.predict(Btest)

y_pred_A

y_pred_B

Bpred = pd.DataFrame([y_pred_B])

Bpred.info()

"""##6.2) to evaluate with some evaluation methods"""

plt.scatter(y_test_A,y_pred_A)

plt.scatter(y_test_B,y_pred_B)

rmse_A = metrics.mean_squared_error(y_test_A, y_pred_A, squared=False)
print("RMSE)_A = ", rmse_A)

rmse_B = metrics.mean_squared_error(y_test_B, y_pred_B, squared=False)
print("RMSE)_B = ", rmse_B)

mape_A = np.mean(np.abs((y_test_A - y_pred_A) / y_test_A)) * 100
print("MAPE_A = ", mape_A, "%")

mape_B = np.mean(np.abs((y_test_B - y_pred_B) / y_test_B)) * 100
print("MAPE_B = ", mape_B, "%")

from sklearn.metrics import r2_score

r2_score_A = r2_score(y_test_A, y_pred_A)
print("R2_A = ", r2_score_A)

r2_score_B = r2_score(y_test_B, y_pred_B)
print("R2_B = ", r2_score_B)