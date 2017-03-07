from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
import numpy as np
import pandas as pd
dataframe = pd.read_csv("ML_Data.csv")
dataset = dataframe.values
columns = dataframe.columns.tolist()
# Filter the columns to remove ones we don't want.
columns = [c for c in columns if c not in ["MSISDN", "mod_class","total_degree"]]
temp = dataframe.sample(frac=1.0)
data = temp[columns]
print data.shape
print columns[0],columns[1],columns[2]

data2 = np.array(data)
print len(data2), len(data2[3])
#data = array(randint(10,size=(10,3)))

results = PCA(data)
#print results.fracs

#print results.Wt

#this will return a 2d array of the data projected into PCA space
print results.Y 

x = []
y = []
z = []
for item in results.Y:
	x.append(item[0])
	y.append(item[1])
	z.append(item[2])

fig1 = plt.figure() # Make a plotting figure
ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object.
'''pltData = [x,y,z] 
ax.scatter(pltData[0], pltData[1], pltData[2], 'bo') # make a scatter plot of blue dots from the data
xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.
'''
ax.scatter(data[columns[0]],data[columns[1]],data[columns[2]])
# label the axes 
ax.set_xlabel("In-Degree") 
ax.set_ylabel("Out-Degree")
ax.set_zlabel("Credit Count")
ax.set_title("Original Data")
plt.show()