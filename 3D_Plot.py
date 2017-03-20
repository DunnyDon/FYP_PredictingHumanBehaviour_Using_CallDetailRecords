'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pymongo
from pymongo import MongoClient
import math
import pandas as pd
from sklearn import preprocessing
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.Users_Degree

cursor = collect.find({"$and": [{"CredCount":{"$gt":0}},{"out_degree":{"$gt":0}}]},{'CredCount':1,'out_degree':1,'in_degree':1,'_id':0}, no_cursor_timeout=True)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
'''data = list(cursor)
print data["CredCount"]
df = pd.DataFrame(data)
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(df)
df_normalized = pd.DataFrame(np_scaled)

'''
# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c in cursor:
	xs = c["in_degree"]
	ys = c["out_degree"]
	zs = c["CredCount"]
	ax.scatter(xs, ys, zs, 'r')

ax.set_xlabel('In Degree')
ax.set_ylabel('Out Degree')
ax.set_zlabel('CredCount')

plt.show()
