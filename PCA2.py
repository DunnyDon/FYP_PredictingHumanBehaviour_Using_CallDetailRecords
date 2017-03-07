import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
#matplotlib inline

#Load data set
data = pd.read_csv('ML_Data.csv')

#convert it to numpy arrays
X=data.values
columns = data.columns.tolist()
# Filter the columns to remove ones we don't want.
columns = [c for c in columns if c not in ["MSISDN"]]
#Scaling the values
X = data[columns]
print X.shape
X = scale(X)

pcb = PCA()
pcb.fit(X)
var= pcb.explained_variance_ratio_
print "All Components ",var
var1=np.cumsum(np.round(pcb.explained_variance_ratio_, decimals=4)*100)
print var1
print pcb.explained_variance_
figu = plt.figure(1)
plt.plot(var1, 'go')
plt.xlabel("PCA")
plt.ylabel("Cumulative Proportion of Variance Explained")
figu.show()

pca = PCA(n_components=2)
var= pcb.explained_variance_ratio_
print "With 2 Components ",var
pca.fit(X)
X1=pca.fit_transform(X)
existing_df_2d = pd.DataFrame(X1)
#existing_df_2d.index = X1.index
existing_df_2d.columns = ['PC1','PC2']
print existing_df_2d

fig = plt.figure(2)
plt.plot(X1,'o')
plt.title("PCA Layers Plotted")
plt.xlabel("Sample Number")
fig.show()
fi = plt.figure(3)
plt.scatter(X1[:,1],X1[:,0])
plt.ylabel('PCA 0 ')
plt.xlabel('PCA 1')
plt.title('PCA VS PCA')
fi.show()
plt.show()
'''
#The amount of variance that each PC explains
var= pca.explained_variance_ratio_
print var
#Cumulative Variance explains
var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
print var1
#plt.scatter(var1)
plt.show()
#Looking at above plot I'm taking 30 variables
pca = PCA(n_components=2)
pca.fit(X)	
X1=pca.fit_transform(X)

print X1
plt.plot(X1,'o')
plt.show()
'''