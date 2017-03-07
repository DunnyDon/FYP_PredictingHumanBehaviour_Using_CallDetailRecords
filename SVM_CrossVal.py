import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
import pandas as pd
from sklearn.model_selection import cross_val_score
dataframe = pd.read_csv("ML_Data.csv")
dataset = dataframe.values
# split into input (X) and output (Y) variables

#print dataframe.columns, dataframe.shape

columns = dataframe.columns.tolist()
# Filter the columns to remove ones we don't want.
data = [c for c in columns if c not in ["MSISDN", "mod_class","CredCount"]]
target = [c for c in columns if c not in ["MSISDN", "mod_class","in_degree","out_degree","total_degree"]]
print target
all_data = dataframe.sample(frac=1)
x_data = all_data[data]
y_data = all_data[target]
y_data = pd.DataFrame.as_matrix(y_data).ravel()
print x_data.shape,y_data.shape
# Store the variable we'll be predicting on.
X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.4, random_state=0)
# Initialize the model class.

clf = svm.SVC(kernel = 'linear',C = 2.5,gamma = 1) # Passing C = 1.1 to SVC improves the results

scores = cross_val_score(clf, x_data, y_data, cv=3)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
