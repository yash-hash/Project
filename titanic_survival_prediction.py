# -*- coding: utf-8 -*-
"""Titanic survival prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eDUbTp1WtBAKrhi6tMuHDbmmbtX2NSdt
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing the Libraries
import numpy as np
import pandas as pd
import seaborn as sns
# %matplotlib inline

train = pd.read_csv('train.csv')

# Visualising Data
print(train.info()) # total information about the passengers
print(train.head()) # top 5 values of dataframe
print(train.describe()) #statiscal data analysis
print(train.count()) 
print(train.columns.tolist())

# Count of Female
train[train['Sex'].str.match('female')].count()

# Count of Male
train[train['Sex'].str.match('male')].count()

# People survived by class
sns.countplot(x='Survived', hue ='Pclass', data=train)

# People survived by Sex
sns.countplot(x="Survived", hue="Sex",data=train)

#function for imputing ages regarding the corresponding age average per class

def add_age(cols):
  Age = cols[0]
  Pclass = cols[1]
  if pd.isnull(Age):
    return int(train[train["Pclass"] == Pclass]["Age"].mean())
  else:
    return Age
plt.figure(figsize=(10,7))
sns.boxplot(x = "Pclass",y="Age",data=train)

#Calling the Funciton
train["Age"] = train[["Age","Pclass"]].apply(add_age,axis=1)
print(train["Age"])

# Data Deletion for incomplete values
train.drop('Cabin', axis=1 ,inplace=True)
train.dropna(inplace=True)
#train.dropna(inplace=True) #Removing rows with null values

# Creating 2 columns, one for female & one for male
pd.get_dummies(train["Sex"])
sex = pd.get_dummies(train["Sex"],drop_first=True)

# Same for Embarked & Pclass
embarked = pd.get_dummies(train["Embarked"],drop_first=True)
Pclass = pd.get_dummies(train["Pclass"],drop_first=True)

# Adding variables to the Dataset
train = pd.concat([train,Pclass,sex,embarked],axis=1)
train

# Removing columns we are going to use for our model
train = train.drop(["PassengerId","Pclass","Name","Sex","Ticket","Embarked",],axis=1)

# Model creation
# x contains all the features
# y contains the target values
x = train.drop("Survived",axis=1)
y = train["Survived"]

# Splitting the data into training & Testing data
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.3, random_state = 101)

# Training the model using LogisticRegression
from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression()
logmodel.fit(x_train,y_train)

#Checking the model prediction
predictions = logmodel.predict(x_test)
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))
print(accuracy_score(y_test,predictions)*100)

