import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.FYP_Capped_Data
#new_collection = db.FYP_USSD_Codes
new_collection = db.FYP_USSD_Unique_Codes
percent = 0.0
count = 0.0
#cursor = collect.find({'$and':[{"key":re.compile('.*\*.*')},{"key":re.compile('.*\#.*')}]})
cursor = collect.find()
ussdarray = cursor[:]
total = cursor.count()
for i in ussdarray:
	count+=1
	if i["USSD"].startswith('*') and i["USSD"].endswith('#'):
		if new_collection.find({"USSD":i["USSD"]}).count == 0:
			print "in here"
			new_collection.insert({"USSD":i["USSD"]})
			if int((count/total)*100) != int(percent): 
				percent = (count/total)*100
				print int(percent), '%'
		else:
			print 'not'
client.close()

