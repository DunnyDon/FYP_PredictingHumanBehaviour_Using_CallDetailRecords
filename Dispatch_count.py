import pymongo
from pymongo import MongoClient
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.FYP_Data
new_collection = db.FYP_USSD_Codes
#connect to the database and the correct collection
percent = 0.0
count = 0.0
# there was an error with the cursor id not being found this was worked around
#by skipping to the % where it last failed
# I think the failure was due to putting the laptop to sleep when it had to be closed
cursor = collect.find({},{'_id':0,'USSD':1})
ussdarray = cursor[:]
total = cursor.count()
dispatch_count = 0

for i in ussdarray:
	count+=1
	code = i["USSD"] 
	if code.startswith('*') and code.endswith('#'): #make sure it is a valid ussd code
		if code.count("*")>1:
			new_code = code.split("*")
			#some codes contained vouchers and were not in the format *xxx# 
			#this has to be adjusted for so the original number xxx can be got and saved
			code = new_code[1]
			if '#' in code:
				dispatch_count +=1
				if int((count/total)*100) != int(percent): 
					percent = (count/total)*100
					print int(percent), '%'
					print "Total to Dispatch so far ", dispatch_count
client.close()

