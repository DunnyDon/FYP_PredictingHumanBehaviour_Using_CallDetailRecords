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
train = dataframe.sample(frac=0.8)
# Select anything not in the training set and put it in the testing set.
test = dataframe.loc[~dataframe.index.isin(train.index)]
# Print the shapes of both sets.
X_train = train[columns]
Y_train = train[target]
X_test = test[columns]
Y_test = test[target]
# Initialize the model class.
model = LinearRegression()
# Fit the model to the training data.
model.fit(X_train, Y_train)
# Generate our predictions for the test set.
predicted = model.predict(X_test)
expected = Y_test
mse = mean_squared_error(predicted, expected)
# summarize the fit of the model
print mse

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