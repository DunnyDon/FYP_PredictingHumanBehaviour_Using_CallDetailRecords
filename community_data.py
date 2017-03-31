import pymongo
from pymongo import MongoClient
import re,threading
import matplotlib.pyplot as plt
import math
f = open("Community_Data.txt",'a')
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.Weighted_Users
community_data = {}
community_data["CredCount"]={}
community_data["TopUp"] = {}
num_of_communities = 25
for i in range(0,22):
	community_data["CredCount"][i]= 0
	community_data["TopUp"][i] = 0
print "Starting........."
for j in range(0,22):
	community_size = collect.find({"$and": [{"mod_class":j},{"CredCount":{"$gt":0}},{"out_degree":{"$gt":0}}]},{'CredCount':1,'out_degree':1,'_id':0}).count()
	#community_size = collect.find({"mod_class":j},{'CredCount':1,'out_degree':1,'_id':0}, no_cursor_timeout=True)
	#cursor = collect.find({"$and": [{"mod_class":j},{"CredCount":{"$ne":0}},]},{'CredCount':1,'out_degree':1,'_id':0}, no_cursor_timeout=True)
	cursor = collect.find({"$and": [{"mod_class":j},{"CredCount":{"$gt":0}},{"out_degree":{"$gt":0}}]},{'CredCount':1,'out_degree':1,'_id':0}, no_cursor_timeout=True)
	#{"$and": [{"mod_class":j},{"CredCount":{"$ne":"0"}},{"out_degree":{"$ne":"0"}}]}
	count_topups = 0
	count_callmes = 0	
	for i in cursor:
		count_topups +=i["CredCount"]
		count_callmes += i["out_degree"]
	community_data["CredCount"][j] = count_topups/(float(community_size))
	community_data["TopUp"][j] = count_callmes/(float(community_size))
	to_write = "Community "+str(j)+ " Credit "+ str(count_topups/(float(community_size)))+" Call me Back "+str(count_callmes/(float(community_size)))+ " Size "+ str(community_size)
	print to_write
	f.write(str(to_write)+'\n')
data_dict =community_data["CredCount"]
def get_mean(data_diction):
	sum = 0.0
	for y in data_diction:
		sum+=data_diction[y]
	mean = sum/len(data_diction)
	return mean
def get_std_deviation(data_diction,mean):
	dev_cred=0
	dev_top =0
	temp=0.0
	temp_sqrd=0.0
	str()
	#print data_dict.keys()
	#print data_dict.values() 
	for z in data_diction:
		temp = data_diction[z]-mean
		temp_sqrd += math.pow(temp,2)
	temp_sqrd = temp_sqrd/len(data_dict)
	std_dev = math.sqrt(temp_sqrd)
	return std_dev
mean_cred = get_mean(data_dict)
cred_dev = get_std_deviation(data_dict,mean_cred)
mean_top = get_mean(community_data["TopUp"])
topUp_dev = get_std_deviation(community_data["TopUp"],mean_top)
print "Mean:"
print "\tCredit ", mean_cred
print "\tTop Up ", mean_top
print "Standard Deviations:"
print "\tCredit ", cred_dev
print "\tTop Up ", topUp_dev
std_dev_write_cred = "Standard Deviations:\n\tCredit "+str(cred_dev)+"\n\tTop Up "+ str(topUp_dev)
std_dev_write_top = "Mean:\n\tCredit "+str(mean_cred)+"\n\tTop Up "+ str(mean_top)
f.write(std_dev_write_top)
f.write(std_dev_write_cred)
x = data_dict.keys()
y = data_dict.values()
cred = plt.figure(1)
plt.scatter(x,y)
plt.xlabel('Commmunity Number')
plt.ylabel('Normalised Total')
av = plt.axhline(y=mean_cred, color='k')
plt.title('Average Top Ups per community')
plt.legend([av],["Average"])
cred.show()
data =community_data["TopUp"]
x_topup = data.keys()
y_topup = data.values()

cmb = plt.figure(2)
plt.scatter(x_topup,y_topup,color='r')
#plt.legend([cred,cmb],["Credit Top Ups","Call Me Back Request"])
plt.title('Average Call me Back Requests')
plt.xlabel('Commmunity Number')
plt.ylabel('Normalised Total')
avgr = plt.axhline(y=mean_top, color = 'g')
plt.legend([avgr],["Average"])
cmb.show()
#plt.axis([0,50000, -250,1300])
plt.show()
f.close()