from __future__ import print_function
import collections
import scipy.stats as stats
import re,statistics
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.Big_Comp_Users
credcollect = db.CallMe_TopUp
wealth_rules = db.wealth_standards
credit_regex = '^\*130'
cred = re.compile(credit_regex)
cursor = collect.find({"CredCount":{"$gt":0}},{'_id':0,'CredCount':1})
max = 0.0
dt = []
for i in cursor:
	temp = i["CredCount"]
	dt.append(temp)
	if temp > max:
		max = float(temp)
dt.sort(reverse=True)
print("Max value found is "+str(max))
def wealth_percentile(data):
	no_duplicates = list(set(data))
	wealth_keys = np.arange(0,100,20)
	users_wealth = dict.fromkeys(wealth_keys, 0)
	calc_temp=0
	for j in data:
		if j!=calc_temp:
			percentile_value = stats.percentileofscore(no_duplicates, j)
			calc_temp=j
		if (percentile_value)>80:
			users_wealth[80] +=1
		elif (percentile_value)>60:
			users_wealth[60] +=1
		elif (percentile_value)>40:
			users_wealth[40] +=1
		elif (percentile_value)>20:
			users_wealth[20] +=1
		else:
			users_wealth[0] +=1

			
	plt.figure(2)
	od = collections.OrderedDict(sorted(users_wealth.items()))

	for k, v in od.iteritems():
		plt.bar(k, v,10)
		print(str(k)+"\t"+str(v))
		
	print(statistics.median(data))
	plt.xticks(od.keys(),('Poor', 'Below Average', 'Average', 'Above Average', 'Rich'))
	plt.xlabel('Wealth')
	plt.ylabel('Number of Users')
	plt.title('Wealth Distribution based on Percentile')
	

def wealth_distribution(data):
	plt.figure(1)
	no_duplicates = list(set(data))
	users_wealth = dict.fromkeys(no_duplicates, 0)
	for inc in data:
		users_wealth[inc]+=1
	plt.title('Distribution based on Amount of Credit Top Ups')
	plt.xlabel('Number of Credit Top Ups')
	plt.ylabel('Number of Users who topped up x amount')
	plt.plot(users_wealth.keys(),users_wealth.values())

wealth_distribution(dt)	
wealth_percentile(dt)
print('Mean value of data is '+str(statistics.mean(dt)))
plt.show()
# Maybe use interquartile range for 
# dividing into groups??
#
#
# However if threshold is broken it must be wait until the amount of 
# Credit top ups change, ie. two people with the same amount of top ups
# must have the same Classification 
# 