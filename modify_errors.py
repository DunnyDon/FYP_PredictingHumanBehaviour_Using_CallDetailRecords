import pymongo
from pymongo import MongoClient
import re
import json
import threading
import time
from collections import defaultdict
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
ussd_codes = db.FYP_USSD_Codes
session_array = []
ussd_dict = {}
us_code_array =[]
find_errors=["error","not authorized","not eligible","not qualified","don't qualify","unknown service","wrong short code","already subscribed","technical difficulties", "invalid","try again","unavailable","failed","no httpcontext","wrong input","access denied","not registered","Your not a user yet...GET OUT!","you are not part of","you are not a postpaid subscriber","not available","no message"]
#initialise all variables and open a file to write the responses too

#create your functions before you call them

def modify_entries(response):
	for e in find_errors:
		if e in response["USSD"].lower():
			everything.update({"$and": [{"CDRID":response["CDRID"]},{"Trans":"2"}]},{'$set':{"ignore":"1"}})
			everything.update({"$and": [{"CDRID":response["CDRID"]},{"Trans":"1"}]},{'$set':{"ignore":"1"}})
			#print response["Date"],' ',response["Time"]
			#print response["USSD"], response["CDRID"]

def get_session_id(skp):
	count = 0
	index=0
	b=0
	threads=[]
	num_limit = 10000
	#get a limited amount of cdr ids relating to the ussd codes 
	#max_count = everything.find({"Trans":"1"},{'_id':0,'CDRID':1,'USSD':1,'Time':1,'Date':1}).count()
	#max_count = 196573263
	cdr_id_cursor = everything.find({"$and": [{"Status":{'$eq':"0"}},{"Trans":"2"},{"ignore":{'$ne':"1"}}]},{'_id':0,'CDRID':1,'Time':1,'Date':1,'USSD':1}).limit(1000000).skip(skp*10000)
	for cdr_index in cdr_id_cursor:
		if b%10000==0:
			print cdr_index["Time"], " ",cdr_index["Date"]
		b+=1
		#thread.start_new_thread(delete_entries,(cdr_index))
		t= threading.Thread(target = modify_entries, args=(cdr_index,))
		threads.append(t)
	for thre in threads:
		index = index+1
		thre.start()
		if(index%num_limit==0):
			for x in threads[count:index]:
				x.join()
				#print threading.activeCount()                                
			count = index
			print index
			
loopind=0
while loopind<40:			
	get_session_id(36+(loopind*1000))
	print loopind
	loopind+=1
	
client.close()				
'''> db.FYP_Data.find({$and: [{"Status":{'$eq':"0"}},{"Trans":"2"}]}).count()
>151,924,213'''