#moved the CredCount to the degree collection so they 
#could be combined together

import pymongo,threading,re
from pymongo import MongoClient
from datetime import datetime, date, time
import matplotlib.pyplot as plt
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.Big_Comp_Users
topUp_db = db.CallMe_TopUp
users = []
top_count={}
def get_users():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	users = []
	cursor = collect.find({},{'_id':0,'MSISDN':1})
	for j in cursor:
		users.append(j["MSISDN"])
	#get your ussd codes
	return users

def update_collection(usr_dict):
	for u in usr_dict:
		collect.update({"MSISDN":u},{"$set":{"CredCount":top_count[u]}})

		
print "Starting Now..........."
users = get_users()
top_count = top_count.fromkeys(users,0)
ussd_regex = '^\*130'
ussd = re.compile(ussd_regex)
count = 0
cursor = topUp_db.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'USSD':1,'MSISDN':1,'_id':0}, no_cursor_timeout=True)
#The no cursor timeout solved the issue of 'no cursor found' Error
#.addOption(DBQuery.Option.exhaust)
#,cursor_type=CursorType.EXHAUST
print "Begin loop through Data...."
for i in cursor:
	count +=1
	temp_user = i["MSISDN"]
	#if temp_user in users:
	try:
		top_count[temp_user] +=1
	except KeyError as e:
		z=e
		#print temp_user,top_count[temp_user]
	if count%1000000 == 0:
		print count
update_collection(top_count)

