from sklearn.svm import SVC
import numpy as np
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,accuracy_score
import matplotlib.pyplot as plt
dataframe = pd.read_csv("ML_Data.csv")
dataset = dataframe.values
# split into input (X) and output (Y) variables

#print dataframe.columns, dataframe.shape

print dataframe.corr()["CredCount"]
columns = dataframe.columns.tolist()
# Filter the columns to remove ones we don't want.
columns = [c for c in columns if c not in ["MSISDN", "mod_class"]]

# Store the variable we'll be predicting on.
target = "CredCount"
train = dataframe.sample(frac=0.66, random_state=1)
# Select anything not in the training set and put it in the testing set.
test = dataframe.loc[~dataframe.index.isin(train.index)]
# Print the shapes of both sets.
X_train = train[columns]
y_train = train[target]
X_test = test[columns]
y_test = test[target]
# Initialize the model class.

clf = SVC(kernel = 'linear',C = 2.5,gamma = 1) # Passing C = 1.1 to SVC improves the results

clf.fit(X_train.values, y_train.values) # Trains the classifier. If you want to use this in real life,
#clf.fit(X=test.values, y=target.values)
# you should replace X_train, y_train with X, y to use the whole dataset to train on.


score = clf.score(X_test, y_test) * 100 # The score method tried to predict the values for X_test and compares them to
# y_test. This returns a number between 0 and 1 that represents what part of the values was predicted right.
# I then multiply that number by 100 to get a percentage.
print("The accuracy is {}%".format(score)) # The average score is ~97.7%

'''
plt.scatter(dataframe["CredCount"],dataframe["in_degree"])
plt.xlabel('Credit Top Ups')
plt.ylabel('Number of Call me Back Requests Initiated')
plt.title('Relationship between Call me back request and Credit Top up')
plt.axis([2,512, 2,256])
#plt.xscale('log')
#plt.yscale('log',basey=2)

plt.show()

'''