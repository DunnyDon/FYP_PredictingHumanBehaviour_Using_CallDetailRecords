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
#initialise all variables and open a file to write the responses too

#create your functions before you call them

def get_ussd_codes():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0}).limit(2)
	for j in cursor:
		uscodearr.append(j)
	#get your ussd codes
	return uscodearr
	
	
def delete_entries(cdr_index):
	if cdr_index["Error"]!="0":
		everything.delete_one({"$and": [{"CDRID":cdr_index["CDRID"]},{"Trans":"2"}]})
		everything.delete_one({"$and": [{"CDRID":cdr_index["CDRID"]},{"Trans":"1"}]})
		print 'Error ',cdr_index["CDRID"], '\t', cdr_index["Date"], '\t', cdr_index["Time"],' '
		

def get_session_id():
	count = 0
	index=0
	threads=[]
	num_limit = 675
	#get a limited amount of cdr ids relating to the ussd codes 
	#max_count = everything.find({"Trans":"1"},{'_id':0,'CDRID':1,'USSD':1,'Time':1,'Date':1}).count()
	#max_count = 196573263
	cdr_id_cursor = everything.find({"$and": [{"Error":{'$ne':"0"}},{"Trans":"2"}]},{'_id':0,'CDRID':1,'Time':1,'Date':1,'Error':1}).skip(6).limit(10000)
	for cdr_index in cdr_id_cursor:
		#thread.start_new_thread(delete_entries,(cdr_index))
		t= threading.Thread(target = delete_entries, args=(cdr_index,))
		threads.append(t)
	for thre in threads:
		index = index+1
		thre.start()
		if(index%num_limit==0):
			for x in threads[count:index]:
				x.join()
				#print threading.activeCount()                                
			count = index

loopindex=0			
while loopindex<300:
	get_session_id()
	loopindex+=1
client.close()				
