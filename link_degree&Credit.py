import pymongo,threading,re
from pymongo import MongoClient
from datetime import datetime, date, time
import matplotlib.pyplot as plt
client = MongoClient()
db = client.FYP_Demo
collect = db.Degree_Credit_Demo
topUp_db = db.Weighted_Users_Degree
users = []
top_count={}
def get_users():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	users = {}
	cursor = collect.find({},{'_id':0})
	for j in cursor:
		users[j["MSISDN"]] = j["CredCount"]
		#print j["CredCount"]
	#get your ussd codes
	return users



def update_collection(usr_dict):
	count = 0 
	for u in usr_dict:
		#print top_count[u]
		count+=1
		if count%10000==0:
			print count
		topUp_db.update({"MSISDN":u},{"$set":{"CredCount":top_count[u]}})

print 'Get users'
top_count=get_users()
print 'Update collection'
update_collection(top_count)