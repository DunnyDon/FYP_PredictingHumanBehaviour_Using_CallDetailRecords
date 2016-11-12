import pymongo
from pymongo import MongoClient
import re
import json
from collections import defaultdict
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
ussd_codes = db.FYP_USSD_Codes
limit = 1
num = 1
session_array = []
ussd_dict = {}
us_code_array =[]
f = open('C:\Users\Conor\Desktop\USSD_Responses_with_Errors.txt','a')
ussd_others = {}				
def ussd_message(sesarr, ussdiction):
	for j in sesarr:
		session_cursor = everything.find({"$and": [{"CDRID":j},{"Trans":"2"}]},{'_id':0,'USSD':1}).limit(1)
		code = ussdiction[j] 
		for k in session_cursor:
			if(len(code)==5):
				#print ussdiction[j],'\t',k["USSD"],"\t",j
				#linetowrite = str(ussdiction[j],'\t',k["USSD"],"\t",j)
				f.write(ussdiction[j]+'\t'+k["USSD"]+"\t"+j+'\n')
				fyp = "String"
			elif code.startswith('*') and code.endswith('#'): 
				#make sure it is a valid ussd code
				if code.count("*")>1:
					new_code = code.split("*")
					#some codes contained vouchers and were not in the format *xxx# 
					#this has to be adjusted for so the original number xxx can be got and saved
					split_code = new_code[1]
					if split_code in ussd_dict:
						ussd_dict[split_code] +=1
						
					else:
						ussd_dict[split_code] = 1
						ussd_others.setdefault(split_code,[]).append(k["USSD"])
					if ussd_dict[split_code] <=10:
						ussd_others.setdefault(split_code,[]).append(k["USSD"])
				#print ussdiction[j],'\t',k["USSD"],"\t",j				
	f.write(json.dumps(ussd_others, indent=4))
	#loop through the session ids and find the ussd response to it and return the ussd message
	
def get_ussd_codes(lim):
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0})
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

	
us_code_array = get_ussd_codes(limit)
get_session_id(us_code_array)
f.close()
				
