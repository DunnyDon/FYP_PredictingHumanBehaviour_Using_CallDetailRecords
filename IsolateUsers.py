import pymongo,threading,re
from lockfile import LockFile
from pymongo import MongoClient
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.CallMe_TopUp
new_collection = db.FYP_IsoUsers

def get_users(wh):
	ski = wh*60000
	#cursor = collect.find({},{'MSISDN':1,'_id':0}).skip(ski).limit(50000).batch_size(60000)
	cursor = collect.find({"Trans":"1"},{'MSISDN':1,'_id':0}).batch_size(100000)
	total = cursor.count()
	userarray = cursor[:]
	count=ski
	percent=-1
	for i in userarray:
		count+=1
		if new_collection.find({"MSISDN":i["MSISDN"]}).count()==0:
				new_collection.update({"MSISDN":i["MSISDN"]},{"MSISDN":i["MSISDN"]}, True)
		if count%10000==0:
			print count
			if int((count/total)*100) != int(percent): 
				percent = (count/total)*100
				print int(percent), '%'

lim=0
#while lim <10000:				
get_users(lim)
#	lim+=1
client.close()