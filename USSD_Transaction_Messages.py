import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
ussd_codes = db.FYP_USSD_Codes
cursor = ussd_codes.find()
ussd_codes_array = cursor[:]
count = 0
for i in ussd_codes_array:
	count+=1
	print i["USSD"]
	ussd = re.compile(i["USSD"])
	ussd_cursor = everything.find({"USSD":{"$regex":ussd}}).limit(1)
	transactions = ussd_cursor[:]
	for j in transactions:
		print j['SesID']
		session = j['SesID']
		session_cursor = everything.find({"USSD":session}).limit(2)
		for k in session_cursor:
			print k
		#break
	if count == 3:
		break
