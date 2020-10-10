# -*- coding: utf-8 -*-
"""HR_Ratnesh_github.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18XO6D0WfRn_x3zuC4WHXcY2iG57p-Kdd

<a href="https://colab.research.google.com/github/Ratnesh108/Data-Science-Real-WorldProject/blob/master/HR_Ratnesh.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

#TASK 1: UNDERSTAND THE PROBLEM STATEMENT AND BUSINESS CASE 
HR team collected extensive data on their employee and need a model that could predict which employee is more lickly to be quit

# TASK 2 : IMPORT LIBRARIES AND DATASETS
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# we need to mount our drive using the following commands:
# For more information regarding mounting, please check this out: https://stackoverflow.com/questions/46986398/import-data-into-google-colaboratory

from google.colab import drive
drive.mount('/content/drive')

# You have to include the full link to the csv file containing your dataset
employee_df = pd.read_csv('/content/drive/My Drive/Human_Resources.csv')

employee_df.head()

employee_df.head(5)

employee_df.tail(10)

employee_df.info()
# 35 features in total, each contains 1470 data points

employee_df.describe()

"""# TASK #3: VISUALIZE DATASET"""

# Let's replace the 'Attritition' and 'overtime' column with integers before performing any visualizations 
employee_df['Attrition'] = employee_df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
employee_df['OverTime'] = employee_df['OverTime'].apply(lambda x: 1 if x == 'Yes' else 0)
employee_df['Over18'] = employee_df['Over18'].apply(lambda x: 1 if x == 'Y' else 0)

employee_df.head(4)

employee_df.isnull().sum()  ## simple method to check null value

# Let's see if we have any missing data, luckily we don't! if it could be there will show on white part
sns.heatmap(employee_df.isnull(), yticklabels = False, cbar = False, cmap="Blues")

employee_df.hist(bins=25,figsize=(20,20),color="g")
# Several features such as 'MonthlyIncome' and 'TotalWorkingYears' are tail heavy
# It makes sense to drop 'EmployeeCount' and 'Standardhours' since they do not change from one employee to the other

# It makes sense to drop 'EmployeeCount' , 'Standardhours' and 'Over18' since they do not change from one employee to the other
# Let's drop 'EmployeeNumber' as well
employee_df.drop(['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber'], axis=1, inplace=True)

employee_df

## lets chech wether all 4 colums has dropped or not 
employee_df.shape

# Let's see how many employees left the company!  lets create the two data frames 
left_df        = employee_df[employee_df['Attrition'] == 1]
stayed_df      = employee_df[employee_df['Attrition'] == 0]

# Count the number of employees who stayed and left
# It seems that we are dealing with an imbalanced dataset 

print("Total =", len(employee_df))

print("Number of employees who left the company =", len(left_df))
print("Percentage of employees who left the company =", 1.*len(left_df)/len(employee_df)*100.0, "%")
 
print("Number of employees who did not leave the company (stayed) =", len(stayed_df))
print("Percentage of employees who did not leave the company (stayed) =", 1.*len(stayed_df)/len(employee_df)*100.0, "%")

left_df.describe()

# Let's compare the mean and std of the employees who stayed and left 
# 'age': mean age of the employees who stayed is higher compared to who left
# 'DailyRate': Rate of employees who stayed is higher
# 'DistanceFromHome': Employees who stayed live closer to home 
# 'EnvironmentSatisfaction' & 'JobSatisfaction': Employees who stayed are generally more satisifed with their jobs
# 'StockOptionLevel': Employees who stayed tend to have higher stock option level

stayed_df.describe()

correlations =employee_df.corr()
f,ax  =plt.subplots(figsize=(20,20))
sns.heatmap(correlations,annot=True)

# Job level is strongly correlated with total working hours
# Monthly income is strongly correlated with Job level
# Monthly income is strongly correlated with total working hours
# Age is stongly correlated with monthly income
###################################################################  we can see from color bar the lighter the color more corelated it is

plt.figure(figsize=[20,12])
sns.countplot(x="Age" ,hue="Attrition",data=employee_df)  ## lets check with leaving and stayed candidate with age

## we need columns name  in next graph so try to find the columns name 
employee_df.columns

plt.figure(figsize=[20,20])
plt.subplot(411)   ## 4 row 1 column and plotting the first figure so therefore its (4 1 1) 
sns.countplot(x = 'JobRole', hue = 'Attrition', data = employee_df)

plt.subplot(412)   ## 4 row 1 column and plotting the first figure so therefore its (4 1 2) 
sns.countplot(x = 'MaritalStatus', hue = 'Attrition', data = employee_df)

plt.subplot(413)
sns.countplot(x = 'JobInvolvement', hue = 'Attrition', data = employee_df)

plt.subplot(414)
sns.countplot(x = 'JobLevel', hue = 'Attrition', data = employee_df)

# Single employees tend to leave compared to married and divorced
# Sales Representitives tend to leave compared to any other job 
# Less involved employees tend to leave the company 
# Less experienced (low job level) tend to leave the company

# KDE (Kernel Density Estimate) is used for visualizing the Probability Density of a continuous variable. 
# KDE describes the probability density at different values in a continuous variable. 

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['DistanceFromHome'], label = 'Employees who left', shade = True, color = 'r')
plt.xlabel('Distance From Home')

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['YearsWithCurrManager'], label = 'Employees who left', shade = True, color = 'r')
sns.kdeplot(stayed_df['YearsWithCurrManager'], label = 'Employees who Stayed', shade = True, color = 'b')

plt.xlabel('Years With Current Manager')

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['TotalWorkingYears'], shade = True, label = 'Employees who left', color = 'r')
sns.kdeplot(stayed_df['TotalWorkingYears'], shade = True, label = 'Employees who Stayed', color = 'b')

plt.xlabel('Total Working Years')

## lets try box plot 
## Let's see the Gender vs. Monthly Income
sns.boxplot(x='MonthlyIncome',y ='Gender',data =employee_df)

plt.figure(figsize=(15,10))
sns.boxplot(x ='MonthlyIncome',y='JobRole',data= employee_df)

"""# TASK #4: CREATE TESTING AND TRAINING DATASET & PERFORM DATA CLEANING"""

employee_df.head(3)   ### let see the column data types becouse we need to convert all the categorical column
                      ###  into numerical so we can apply deep learning to it

X_cat = employee_df[['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]
X_cat

## now for convert all this categorical data types into numerical the best library is scikit learn
from sklearn.preprocessing import OneHotEncoder
OHE1 = OneHotEncoder()
X_cat=OHE1.fit_transform(X_cat).toarray()

X_cat

X_cat.shape

X_cat = pd.DataFrame(X_cat)

X_cat

# note that we dropped the target 'Atrittion'
X_numerical = employee_df[['Age', 'DailyRate', 'DistanceFromHome',	'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',	'JobLevel',	'JobSatisfaction',	'MonthlyIncome',	'MonthlyRate',	'NumCompaniesWorked',	'OverTime',	'PercentSalaryHike', 'PerformanceRating',	'RelationshipSatisfaction',	'StockOptionLevel',	'TotalWorkingYears'	,'TrainingTimesLastYear'	, 'WorkLifeBalance',	'YearsAtCompany'	,'YearsInCurrentRole', 'YearsSinceLastPromotion',	'YearsWithCurrManager']]
X_numerical

X_numerical.shape

X_numerical=pd.DataFrame(X_numerical)

X_numerical

X_all = pd.concat([X_cat, X_numerical], axis = 1)
X_all

## going to scale the data before going to feed the artificial nural network
## eg: if suppose any column have data like in 1220,1354, and oher column like 23,12, then while analysing one can dominate others 
## so need to  scale 
from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler()
X =scaler.fit_transform(X_all)

X

X =pd.DataFrame(X)

X

### Putting Target variable seprate 
y = employee_df['Attrition']
y

y.tail(32)

"""# TASK #5: UNDERSTAND THE INTUITION BEHIND LOGISTIC REGRESSION CLASSIFIERS, ARTIFICIAL NEURAL NETWORKS, AND RANDOM FOREST CLASSIFIER

![alt text](https://drive.google.com/uc?id=19DpnhFkfsNEDPlH1dkfdr1zO36vRcBit)

![alt text](https://drive.google.com/uc?id=1J03xZf6OiYtGV3IgJBUURBWyScpvaAbU)

![alt text](https://drive.google.com/uc?id=1WNsznVn7je5r9HGnSLLdABICxrIv2Mrs)

![alt text](https://drive.google.com/uc?id=1bX5uGmy5vbYTlp7m4tw_V2kTNzAHpHLp)

![alt text](https://drive.google.com/uc?id=1ztrMNehNYWMw6NwhOOC9BDBdnoNirpqZ)

# TASK #6: UNDERSTAND HOW TO ASSESS CLASSIFICATION MODELS

![alt text](https://drive.google.com/uc?id=1OZLbKm1AJSyvoBgfvlfcLIWZxLOvzOWq)

![alt text](https://drive.google.com/uc?id=11pNdVw4oWeNOWrkadrrxon7FU4qO5m6U)

![alt text](https://drive.google.com/uc?id=1Bk1xFW2tGBdwg-njOhw79MxtYBQnK-6x)

![alt text](https://drive.google.com/uc?id=19cXoBqSiqbEGNofnD603bz3xEAsX28hy)

# TASK #7: TRAIN AND EVALUATE A LOGISTIC REGRESSION CLASSIFIER
"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

X_train.shape

X_test.shape

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

y_pred

from sklearn.metrics import confusion_matrix, classification_report

print("Accuracy {} %".format( 100 * accuracy_score(y_pred, y_test)))

# Testing Set Performance
cm = confusion_matrix(y_pred, y_test)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_pred))

## now its time to optimize our model

"""# TASK #8: TRAIN AND EVALUATE A RANDOM FOREST CLASSIFIER"""

from sklearn.ensemble import RandomForestClassifier
    
model =RandomForestClassifier()
model.fit(X_train,y_train)

y_pred1 =model.predict(X_test)

y_pred1

# Testing Set Performance
cm = confusion_matrix(y_pred1, y_test)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_pred1))

"""# TASK #9: TRAIN AND EVALUATE A DEEP LEARNING MODEL"""

import tensorflow as tf

## note :- relu means rectified linear units
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=500, activation='relu', input_shape=(50, )))
model.add(tf.keras.layers.Dense(units=500, activation='relu'))
model.add(tf.keras.layers.Dense(units=500, activation='relu'))
model.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

model.summary()

model.compile(optimizer='Adam', loss='binary_crossentropy', metrics = ['accuracy'])

# oversampler = SMOTE(random_state=0)
# smote_train, smote_target = oversampler.fit_sample(X_train, y_train)
# epochs_hist = model.fit(smote_train, smote_target, epochs = 100, batch_size = 50)
epochs_hist = model.fit(X_train, y_train, epochs = 100, batch_size = 50)

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

y_pred

epochs_hist.history.keys()

plt.plot(epochs_hist.history['loss'])
plt.title('Model Loss Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Training Loss')
plt.legend(['Training Loss'])

plt.plot(epochs_hist.history['accuracy'])
plt.title('Model Accuracy Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Training Accuracy')
plt.legend(['Training Accuracy'])

# Testing Set Performance
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_pred))

"""## FINISH CONGRATS"""