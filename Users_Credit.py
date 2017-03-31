#gets top up of each user and plots
from lockfile import LockFile
import pymongo
from pymongo import MongoClient
import re,threading
import matplotlib.pyplot as plt
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.Weighted_Users
topUpCount = []

fle = open('C:\Users\Conor\Documents\FYP\countcredit.csv','a')
def get_users():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	fl = open('C:\Users\Conor\Documents\FYP\usercredit.csv','a')
	users = {}
	cursor = collect.find({},{'_id':0})
	for j in cursor:
		users[j["MSISDN"]] = j["CredCount"]
		#lock = LockFile(fle)
		#with lock:
		temp = str(j["MSISDN"])+","+str(j["CredCount"])+"\n"
		fl.write(temp)
		fl.flush()
		#print j["MSISDN"],"\t",j["CredCount"]
		#get your ussd codes
	fl.close()
	return users

def get_spread_of_topups():
	top_count = {}
	cursor = collect.find({},{'_id':0})
	for i in cursor:
		try:
			top_count[i["CredCount"]] +=1
		except KeyError as e:
			top_count[i["CredCount"]] = 1
	
	tc = top_count
	del tc[0]
	for k,v in tc.iteritems():
		temp = str(k)+","+str(v)
		fle.write(temp+'\n')
	plt.scatter(tc.keys(),tc.values(),color='r')
	#plt.scatter(top_count.keys(),top_count.values(),color='r')
	plt.title('Spread of Credit Top Ups')
	plt.xlabel('Number of Times a user Topped Up')
	plt.ylabel('Number of Users')
	plt.show()
#total = get_users()
get_spread_of_topups()
