import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.FYP_Capped_Data
new_collection = db.FYP_USSD_Codes

percent = 0.0
count = 0.0
cursor = collect.find()
ussdarray = cursor[:]
total = cursor.count()
for i in ussdarray:
	count+=1
	code = i["USSD"] 
	if code.startswith('*') and code.endswith('#'):
		if code.count("*")>1:
			new_code = code.split("*")
			code = new_code[1]
			substringsearch = re.compile(code)
			if new_collection.find({"USSD":{'$regex':substringsearch}}).count()==0:
				new_collection.update({"USSD":code},{"USSD":code}, True)
		else:
			code = code.strip('*').strip('#')
			substringsearch = re.compile(code)
			if new_collection.find({"USSD":{'$regex':substringsearch}}).count()==0:
				new_collection.update({"USSD":code},{"USSD":code}, True)
		if int((count/total)*100) != int(percent): 
			percent = (count/total)*100
			print int(percent), '%'
client.close()

