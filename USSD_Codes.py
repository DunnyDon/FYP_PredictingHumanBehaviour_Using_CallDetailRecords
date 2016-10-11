import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.FYP_Airtel_Storage
collection = db.FYP_Capped_Data
new_collection = db.FYP_USSD_Codes
cursor = collection.find()
total = cursor.count()
percent = 0.0
count = 0.0
USSD_codes = []
for i in cursor:
	count+=1
	if i["USSD"].startswith('*') and i["USSD"].endswith('#') and i["USSD"] not in USSD_codes :
		USSD = i["USSD"]
		new_collection.insert({"USSD":USSD})
		USSD_codes.append(i["USSD"])
	if int((count/total)*100) != int(percent): 
		percent = (count/total)*100
		print int(percent), '%'
client.close()

