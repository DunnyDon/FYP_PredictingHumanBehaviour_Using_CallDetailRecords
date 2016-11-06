import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
ussd_codes = db.FYP_USSD_Codes
limit = 1
skip = 5
count = 0
session_array = []
ussd_dict = {}
us_code_array =[]
def ussd_message(sesarr, ussdiction):
	for j in sesarr:
		session_cursor = everything.find({"$and": [{"CDRID":j},{"Trans":"2"}]},{'_id':0,'USSD':1}).limit(1)
		for k in session_cursor:
			if(len(k["USSD"])==5):
				print ussdiction[j],'\t',k["USSD"],"\t",j

	#loop through the session ids and find the ussd response to it and return the ussd message
	
def get_ussd_codes(sk,lim):
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0}).skip(sk).limit(lim)
	for j in cursor:
		uscodearr.append(j)
	#get your ussd codes
	return uscodearr

def get_session_id(uca):
	sesar = []
	count = 0
	usdiction = {}
	for i in uca:
		count+=1
		ussd = re.compile(i["USSD"])
		ussd_cursor = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'_id':0,'CDRID':1,'USSD':1}).limit(100)
		for k in ussd_cursor:
			usdiction[k['CDRID']] = k['USSD']
			sesar.append(k['CDRID'])
	ussd_message(sesar,usdiction)
	#loop through and associate session ids with ussd codes
	#also save the session ids in an array

	
us_code_array = get_ussd_codes(skip,limit)
get_session_id(us_code_array)

